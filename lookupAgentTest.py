import time
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade import quit_spade
from examples.LookUpAgent import LookUpAgent





if __name__ == "__main__":
    receiveragent = LookUpAgent("spade-sag-dummy@blabber.im", "spadeagent1")
    future = receiveragent.start()
    print(future.result()) # wait for receiver agent to be prepared.
    while receiveragent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            receiveragent.stop()
            break
    print("Agents finished")
    quit_spade()