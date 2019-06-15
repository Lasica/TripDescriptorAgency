from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template
import random

addressBook = {
    "wikipedia": "LookUpAgent2@blabber.im",
    "wikitravel": 'LookUpAgent1@blabber.im',
    "google": "LookUpAgent3@blabber.im"
}



class CallLookupAgentBehaviour(OneShotBehaviour):
    def __init__(self, request, source):
        print(f'{self.__class__.__name__}: init')
        super().__init__()
        self.request = request
        self.source = source

    async def run(self):
        response = self.request.make_reply()

        further_req = Message(to = addressBook.get(self.source))
        further_req.set_metadata("performative" ,"query")

        further_req.body = self.request.body

        await self.send(further_req)

        resp = await self.receive()
        response.body = resp.body

        await self.send(response)

class MainPlacesBehaviour(CyclicBehaviour):
    async def run(self):
        print(f'{self.__class__.__name__}: running')

        req = await self.receive()

        if req:
            source = random.choice(["wikipedia", "wikitravel", "google"])
            mainLookupBehav = CallLookupAgentBehaviour(req, source)

            response_template = Template()#dla danego hehavioura tworzę oddzielny template aby było wiadomo gdzie zwrócić wiadomość
            #TODO dodać zdefiniowanie jakiegoś konkretnego template'a dla zachowania wywołującego danego agenta lookupu aby
            #TODO dispatcher wiedział, gdzie zwrócić wiadomość, rozpropragować tę informację do danego lookupa aby mógł odpowiednio odpowiedzieć
            self.agent.add_behaviour(mainLookupBehav)


class PlacesAgent(Agent):
    async def setup(self):
        print(f'{self.__class__.__name__} started')
        b = MainPlacesBehaviour()
        templates = [Template(sender=address) for address in addressBook.values()]
        template = templates[0]
        for t in templates:
            template = template | t
        self.add_behaviour(b, ~template)


