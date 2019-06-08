import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template
from spade import quit_spade

SenderAgentId   = ["spade-sag-master@blabber.im", "spadeagent0"]
ReceiverAgentId = ["spade-sag-dummy@blabber.im", "spadeagent1"]
PlacesAgentId = ["spade-sag-places@blabber.im", "spadeplaces"]
class PlacesAgent(Agent):
    async def setup(self):
        print("Agent starting . . .")
        b = self.CreateBehav()
        self.add_behaviour(b)

    class CreateBehav(OneShotBehaviour):

            class SenderAgent(Agent):
                class InformBehav(OneShotBehaviour):
                    async def run(self):
                        print("InformBehav running")

                        msg = Message(to=PlacesAgentId[0])  # Instantiate the message
                        msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
                        msg.body = "spaghetto"  # Set the message content

                        await self.send(msg)
                        print("Message sent!")

                        # stop agent from behaviour
                        await self.agent.stop()

                async def setup(self):
                    print("SenderAgent started")
                    b = self.InformBehav()
                    self.add_behaviour(b)


            class ReceiverAgent(Agent):
                class RecvBehav(OneShotBehaviour):
                    async def run(self):
                        print("RecvBehav running")

                        msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
                        if msg:
                            print("Message received with content: {}".format(msg.body))
                        else:
                            print("Did not received any message after 10 seconds")

                        # stop agent from behaviour
                        await self.agent.stop()

                async def setup(self):
                    print("ReceiverAgent started")
                    b = self.RecvBehav()
                    template = Template()
                    template.set_metadata("performative", "inform")
                    self.add_behaviour(b, template)

            async def run(self):
                print("run")
                #receiveragent = self.ReceiverAgent(ReceiverAgentId[0], ReceiverAgentId[1])
                #await receiveragent.start(auto_register = False)
                senderagent   = self.SenderAgent(SenderAgentId[0], SenderAgentId[1])
                await senderagent.start(auto_register = False)
                msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
                if msg:
                    print("Message received with content: {}".format(msg.body))
                else:
                    print("Did not received any message after 10 seconds")

if __name__ == "__main__":
    places = PlacesAgent(PlacesAgentId[0], PlacesAgentId[1])
    future = places.start()
    future.result()

    while places.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            places.stop()
            break
    print("Agents finished")
    quit_spade()


