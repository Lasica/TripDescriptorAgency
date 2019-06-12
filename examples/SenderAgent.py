from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message


class InformBehav(CyclicBehaviour):
    async def run(self):
        print("InformBehav running")

        msg = Message(to="spade-sag-dummy@blabber.im")  # Instantiate the message
        msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
        msg.body = "spaghetto"

        await self.send(msg)
        print("Message sent!")

        msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
        if msg:
            print("Echo Message received with content: {}".format(msg.body))
            await self.agent.stop()
        else:
            print("Did not received any message after 10 seconds")



class SenderAgent(Agent):

    async def setup(self):
        print("SenderAgent started")
        b = InformBehav()
        self.add_behaviour(b)
