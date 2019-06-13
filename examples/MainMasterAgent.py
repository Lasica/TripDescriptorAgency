from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

addressBook = {
    "placesAgent": "PlacesMaster@blabber.im"
}


class MainMasterBehav(CyclicBehaviour):
    async def run(self):
        results = {}
        print(f'{self.__class__.__name__}: running')

        request = await self.receive()#TODO może dodać assert aby rozróżniać wiadomości z żądaniem oraz odpowiedziami?

        if request:

            for contact in addressBook:
                msg = Message(to=addressBook.get(contact))  # Instantiate the message
                msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
                msg.body = request.body
                await self.send(msg)

            for i in range(1,len(addressBook)):
                result = await self.receive()
                results[result.sender] = result.body

            response = Message(to= request.sender)
            response.set_metadata("performative", "inform")
            response.body(results)
            await self.send(response)


class MainMasterAgent(Agent):
    async def setup(self):
        print(f'{self.__class__} started')
        b = MainMasterBehav()
        self.add_behaviour(b)


