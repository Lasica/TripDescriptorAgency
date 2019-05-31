import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template



class ReceiverAgent(Agent):
    class RecvBehav(OneShotBehaviour):
        async def run(self):
            print("RecvBehav running")
            msg = await self.receive(timeout=60)  # wait for a message for 10 seconds
            if msg:
                print("Message received with content: {}".format(msg.body))
            else:
                print("Did not received any message after 60 seconds")
            # stop agent from behaviour
            await self.agent.stop()


    async def setup(self):
        print("ReceiverAgent started")
        b = self.RecvBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)

if __name__ == "__main__":
    receiveragent = ReceiverAgent("spade-sag-dummy@blabber.im", "spadeagent1")
    future = receiveragent.start()
    future.result()  # wait for receiver agent to be prepared.
