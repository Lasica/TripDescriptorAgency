import time
from agents.LookUpAgent import LookUpAgent





if __name__ == "__main__":
    receiveragent = LookUpAgent("spade-sag-dummy@blabber.im", "spadeagent1")
    future = receiveragent.start()
    receiveragent.web.start(hostname="127.0.0.1", port="10000")
    print(future.result()) # wait for receiver agent to be prepared.
    while receiveragent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            receiveragent.stop()
            break
    print("Agents trying to finish")
    #quit_spade()