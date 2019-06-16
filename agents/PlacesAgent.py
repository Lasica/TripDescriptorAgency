from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template
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
        print(self.request)
        print(self.request.body)
    async def run(self):
        response = self.request.make_reply()
        print(self.request.body)
        #tworzymy wiadomość do przekazania do konkretnego agenta
        further_req = Message(to=addressBook.get(self.source))#ustawiamy adresata

        further_req.set_metadata('request_id', self.reqId)#ustawiamy id zapytania: w agencie adresacie wiadomość jest
        # tworzona jako reply żądania, więc request_id pozostanie to samo i odpowiedź trafi do tego konkretnego zachowania
        further_req.body = self.request.body #przekazujemy treść zapytania
        # tworzymy wiadomość do przekazania do konkretnego agenta
        print(further_req.body)
        await self.send(further_req)

        resp = await self.receive()
        print(resp.body)
        print("body1")
        response.body = resp.body# odbieramy streszczenie

        await self.send(response)# odsyłamy streszczenie

class MainPlacesBehaviour(CyclicBehaviour):
    async def run(self):
        #print(f'{self.__class__.__name__}: running')

        req = await self.receive()

        if req:
            print("request")
            print(req.body)
            #source = random.choice(["wikipedia", "wikitravel", "google"])
            source = "wikipedia"
            response_template = Template()#dla danego hehavioura tworzę oddzielny template aby było wiadomo gdzie zwrócić wiadomość
            requestId = uuid.uuid4().hex#tworzymy losowe id zapytania, aby dispatcher
            # mógł rozpoznać konkretny behaviour, do którego ma trafić wiadomość zwrotna
            response_template.metadata = {'request_id': requestId}

            mainLookupBehav = CallLookupAgentBehaviour(req, source, requestId)
            self.agent.add_behaviour(mainLookupBehav, response_template)


class PlacesAgent(Agent):
    async def setup(self):
        print(f'{self.__class__.__name__} started')
        b = MainPlacesBehaviour()
        templates = [Template(sender=address) for address in addressBook.values()]
        template = templates[0]
        for t in templates:
            template = template | t
        self.add_behaviour(b, ~template)


