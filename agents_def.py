import time
from spade.agent import Agent
from spade.message import Message
from spade.template import Template
from spade import quit_spade
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from access_web_resource import Summarizer
from access_web_resource import GoogleSearch
from aioxmpp import Presence

PlacesAgentId = ["spade-sag-places@blabber.im", "spadeplaces"]
SenderAgentId   = ["spade-sag-master@blabber.im", "spadeagent0"]
#główny agent rozsyłający żądania
class SummarizerPlacesAgent(Agent):
    #odbieramy przy starcie informacje o punktach wycieczki
    #format places: [[[1, 'Warsaw'], ['tour', 'history', 'WWII']]]
    def __init__(self, ip, _pass, places, summ_parms):
        Agent.__init__(self, ip, _pass)
        self.places = places
        self.summ_parms = summ_parms

    async def setup(self):
        print("Agent starting . . .")
        b = self.MainBehav()
        self.add_behaviour(b)

    class MainBehav(OneShotBehaviour):
        #definicje kolejnych agentów
            class SingleSummaryAgent(Agent):
                #source - konkretne źródło, strona z której mamy robić wyszukanie
                #place: nazwa miejsca dla którego ma być podsumowanie
                #kwords: słowa kluczowe dla danego miejsca
                #summ_parms: [sentence_len, sentence_num]
                def __init__(self, ip, _pass, source, place, kwords, summ_parms):
                    Agent.__init__(self, ip, _pass)
                    self.source = source
                    self.place  = place
                    self.kwords = kwords
                    self.summ_parms = summ_parms
                    self.connected = False

                class SummarizeAndReturn(OneShotBehaviour):
                    async def run(self):
                        received = False

                        print("SummarizeAndReturn running")

                        #przygotowanie wstępnej zawartości wiadomości
                        msg = Message(to=PlacesAgentId[0])  # Instantiate the message
                        msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative

                        gs = GoogleSearch(self.source + ":" + self.place)
                        summary = Summarizer(*(self.summ_parms))
                        summary_txt = summary.summarize_web_sources(gs.Gsearch())

                        msg.body = summary_txt

                        #while (!received):
                            #await self.send(msg)
                        await self.send(msg)
                        print("Message sent!")

                        # stop agent from behaviour
                        await self.agent.stop()

                async def setup(self):
                    print("SummarizeAndReturn started")
                    b = self.SummarizeAndReturn()
                    self.add_behaviour(b)

            #run głównego zachowania dla agenta
            async def run(self):
                print("MainPlacesRun")
                #print(self.agent.places[1])
                #wikiAgent = self.SingleSummaryAgent(SenderAgentId[0],SenderAgentId[1], "wikipedia", )

                msg = await self.receive()  # wait for a message for 10 seconds
                if msg:
                    print("Message received with content: {}".format(msg.body))
                else:
                    print("Did not received any message after 10 seconds")
                await self.agent.stop()

if __name__ == "__main__":
    place_to_visit = [[[1, 'Warsaw'], ['tour', 'history', 'WWII']]]
    placesAgent = SummarizerPlacesAgent(*PlacesAgentId, place_to_visit, [30, 10])
    future = placesAgent.start()
    future.result()

    while placesAgent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            placesAgent.stop()
            break
    print("Agents finished")
    quit_spade()

