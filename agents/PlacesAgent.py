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

        further_req = Message(to=self.source, metadata={'request_id': self.reqId}, body=self.request.body)

        await self.send(further_req)

        resp = await self.receive(timeout=10)
        print(f'{self.__class__.__name__}: received {resp}')
        if resp:
            response.body = resp.body
        else:
            response.body = "Error"
        await self.send(response)


class MainPlacesBehaviour(CyclicBehaviour):
    async def on_start(self):
        self.sources = [src.lower() for src in addressBook.values()]

    async def run(self):
        print(f'{self.__class__.__name__}: running')

        req = await self.receive(timeout=30)
        print(f'{self.__class__.__name__}: received {req}')

        if req and str(req.sender).split('/')[0] not in self.sources:
            contacts = self.agent.presence.get_contacts()
            #available_sources = [str(address) for address, cinfo in contacts.items() if 'presence' in cinfo]
            available_sources = addressBook['wikipedia']
            print(f'{self.__class__.__name__}: sources {available_sources}')

            source = random.choice(available_sources)
            requestId = uuid.uuid4().hex
            response_template = Template(metadata={'request_id': req.metadata.get('request_id', requestId)})

            mainLookupBehav = CallLookupAgentBehaviour(req, source, req.metadata.get('request_id', requestId))
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


