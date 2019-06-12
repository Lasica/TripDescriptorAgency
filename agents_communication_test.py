import time
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade import quit_spade
from examples.SenderAgent import SenderAgent
from examples.EchoAgent import EchoAgent

SenderAgentId = ["spade-sag-master@blabber.im", "spadeagent0"]



if __name__ == "__main__":
    receiveragent = EchoAgent("spade-sag-dummy@blabber.im", "spadeagent1")
    future = receiveragent.start()
    future.result() # wait for receiver agent to be prepared.
    senderagent = SenderAgent(SenderAgentId[0], SenderAgentId[1])
    senderagent.start()

    while receiveragent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            senderagent.stop()
            receiveragent.stop()
            break
    print("Agents finished")
    quit_spade()
