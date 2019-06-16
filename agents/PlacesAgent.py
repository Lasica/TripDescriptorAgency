from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template
from spade.agent import PresenceManager
from aioxmpp import PresenceType
import random
import uuid

addressBook = {
    "wikipedia": "LookUpAgent2@blabber.im",
    "wikitravel": 'LookUpAgent1@blabber.im',
    "google": "LookUpAgent3@blabber.im"
}

NAMESPACE = uuid.UUID('a0728f87-7e9a-4416-b369-32418a3c1cc8')


class CallLookupAgentBehaviour(OneShotBehaviour):
    def __init__(self, request, source, reqId):
        print(f'{self.__class__.__name__}: init')
        super().__init__()
        self.request = request
        self.source = source
        self.reqId = reqId

    async def run(self):
        response = self.request.make_reply()

        #tworzymy wiadomość do przekazania do konkretnego agenta
        further_req = Message(to=addressBook.get(self.source))#ustawiamy adresata

        further_req.set_metadata('request_id', self.reqId)#ustawiamy id zapytania: w agencie adresacie wiadomość jest
        # tworzona jako reply żądania, więc request_id pozostanie to samo i odpowiedź trafi do tego konkretnego zachowania
        further_req.body = self.request.body #przekazujemy treść zapytania
        # tworzymy wiadomość do przekazania do konkretnego agenta

        await self.send(further_req)

        resp = await self.receive(timeout=10)
        if (resp):
            response.body = resp.body# odbieramy streszczenie
        else:
            response.body = "Błąd"
        await self.send(response)# odsyłamy streszczenie

class MainPlacesBehaviour(CyclicBehaviour):
    async def run(self):
        #print(f'{self.__class__.__name__}: running')

        req = await self.receive(timeout=30)

        if (req and req.sender not in addressBook.values()):
            contacts = self.agent.presence.get_contacts()
            available_sources = [str(address) for address, cinfo in contacts.items() if 'presence' in cinfo]

            source = random.choice(available_sources)
            response_template = Template()#dla danego hehavioura tworzę oddzielny template aby było wiadomo gdzie zwrócić wiadomość
            requestId = uuid.uuid4().hex#tworzymy losowe id zapytania, aby dispatcher
            # mógł rozpoznać konkretny behaviour, do którego ma trafić wiadomość zwrotna
            response_template.metadata = {'request_id': requestId}

            mainLookupBehav = CallLookupAgentBehaviour(req, source, requestId)
            self.agent.add_behaviour(mainLookupBehav, response_template)


class PlacesAgent(Agent):
    async def setup(self):
        print(f'{self.__class__.__name__} started')
        for adress in addressBook:
            self.presence.subscribe(addressBook[adress])
        b = MainPlacesBehaviour()
        templates = [Template(sender=address) for address in addressBook.values()]
        template = templates[0]
        for t in templates:
            template = template | t
        self.add_behaviour(b, ~template)


