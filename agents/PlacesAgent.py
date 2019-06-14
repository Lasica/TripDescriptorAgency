from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template

addressBook = {
    "wikipedia": "LookUpAgent2@blabber.im",
    "wikitravel": 'LookUpAgent1@blabber.im',
    "google": "LookUpAgent3@blabber.im"
}




ckass MainPlacesBehaviour(CyclicBehaviour):
    async def run(self):
        print(f'{self.__class__.__name__}: running')
        
        req = await self.receive()



class PlacesAgent(Agent):
    async def setup(self):
        print(f'{self.__class__.__name__} started')
        b = MainPlacesBehaviour()
        templates = [Template(sender=address) for address in addressBook.values()]
        template = templates[0]
        for t in templates:
            template = template | t
        self.add_behaviour(b, ~template)


