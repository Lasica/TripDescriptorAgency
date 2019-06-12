from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message


class EchoBehav(CyclicBehaviour):
    async def run(self):
        print(f'{self.__class__.__name__}: running')

        msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
        if msg:
            print("Message received with content: {}".format(msg.body))
            reply = msg.make_reply()
            await self.send(reply)
            #await self.agent.stop()

        else:
            print("Did not received any message after 10 seconds")

        # stop agent from behaviour


class EchoAgent(Agent):
    async def setup(self):
        print(f'{self.__class__.__name__} started')
        b = EchoBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)

