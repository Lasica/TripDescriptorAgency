import time
import getpass

from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.behaviour import CyclicBehaviour
from spade import quit_spade
AgentOneId = ["spade-sag-master@blabber.im", "spadeagent0"]
AgentTwoId = ["spade-sag-dummy@blabber.im", "spadeagent1"]

class Agent1(Agent):

    async def setup(self):
        print("Agent {} running".format(self.name))
        self.presence.on_available = self.on_available
        #self.add_behaviour(self.Behav1())
        self.add_behaviour(self.AvalBehav())
        #self.add_behaviour(self.Behav2())


    class AvalBehav(CyclicBehaviour):
        async def run(self):
            print("pierwszy run2!")
            time.sleep(5)

    def on_available(self, jid, stanza):
        print("[{}] Agent {} is available.".format(self.agent.name, jid.split("@")[0]))
        is_second_available = True

    class Behav1(OneShotBehaviour):
        def on_available(self, jid, stanza):
            print("[{}] Agent {} is available.".format(self.agent.name, jid.split("@")[0]))
            is_second_available = True

        def on_subscribed(self, jid):
            print("[{}] Agent {} has accepted the subscription.".format(self.agent.name, jid.split("@")[0]))
            print("[{}] Contacts List: {}".format(self.agent.name, self.agent.presence.get_contacts()))

        def on_subscribe(self, jid):
            print("[{}] Agent {} asked for subscription. Let's aprove it.".format(self.agent.name, jid.split("@")[0]))
            self.presence.approve(jid)

        async def run(self):
            print("pierwszy run!")
            #print(self.presence.get_contacts())
            self.presence.on_subscribe = self.on_subscribe
            self.presence.on_subscribed = self.on_subscribed
            self.presence.on_available = self.on_available

            self.presence.set_available()
            #self.presence.subscribe(self.agent.jid2)

    # class Behav2(CyclicBehaviour):
    #     async def run(self):
    #         self.presence.set_unavailable()
    #         time.sleep(2)
    #         print("aval")
    #         self.presence.set_available()
    #
    #     async def on_end(self):
    #         self.agent.stop()

class Agent2(Agent):
    async def setup(self):
        print("Agent {} running".format(self.name))
        #self.add_behaviour(self.Behav2())
        self.add_behaviour(self.AvalBehav())

    class Behav2(OneShotBehaviour):
        def on_available(self, jid, stanza):
            print("[{}] Agent {} is available.".format(self.agent.name, jid.split("@")[0]))

        def on_subscribed(self, jid):
            print("[{}] Agent {} has accepted the subscription.".format(self.agent.name, jid.split("@")[0]))
            print("[{}] Contacts List: {}".format(self.agent.name, self.agent.presence.get_contacts()))

        def on_subscribe(self, jid):
            print("[{}] Agent {} asked for subscription. Let's aprove it.".format(self.agent.name, jid.split("@")[0]))
            self.presence.approve(jid)
            self.presence.subscribe(jid)

        async def run(self):
            print("drugi run!")
            self.presence.set_available()
            self.presence.on_subscribe = self.on_subscribe
            self.presence.on_subscribed = self.on_subscribed
            self.presence.on_available = self.on_available

    class AvalBehav(CyclicBehaviour):
        async def run(self):
            self.presence.set_unavailable()
            print("A2")
            time.sleep(5)
            self.presence.set_available()

if __name__ == "__main__":

    jid2 = AgentTwoId[0]

    jid1 = AgentOneId[0]


    agent2 = Agent2(AgentTwoId[0], AgentTwoId[1])
    agent1 = Agent1(AgentOneId[0], AgentOneId[1])
    agent1.jid2 = jid2
    agent2.jid1 = jid1
    agent2.start()
    time.sleep(3)# wait for receiver agent to be prepared.
    print("test")
    agent1.start()
    time.sleep(7)
    while True:
       try:
            time.sleep(1)
       except KeyboardInterrupt:
            break
    agent1.stop()
    agent2.stop()
    print("Agents finished")
    #quit_spade()