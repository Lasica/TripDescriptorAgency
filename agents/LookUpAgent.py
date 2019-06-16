from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.template import Template
from WEDT import GoogleSearch, GoogleSummarizer


class LookUpBehaviour(OneShotBehaviour):
    async def run(self):
        print(f'{self.__class__.__name__}: running')

        reply = self.request[0]
        topic = self.request[1]['place']
        keywords = self.request[1]['keywords']

        if reply:
            searchstr = ''
            site = self.get('site')
            if site:
                searchstr = site + ':'
            gs = GoogleSearch(searchstr+topic)
            summary = GoogleSummarizer(*(self.get('summariser_params')), keywords)
            reply.body = summary.summarize_web_sources(gs.Gsearch())
            if (reply.body != 'ERROR'):
                print(reply.body)
            else:
                print("Błąd")
                reply.body = ''
                reply.set_metadata("request", "failed")
            await self.send(reply)
        else:
            print(f'{self.__class__.__name__}: error: reply source does not exist')

    def __init__(self, request):
        print(f'{self.__class__.__name__}: init')
        super().__init__()
        self.request = request



class AwaitRequestBehaviour(CyclicBehaviour):
    async def run(self):
        print(f'{self.__class__.__name__}: running')

        msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
        if msg:
            print(f'{self.__class__.__name__} Message received with content: {msg.body} {msg}')

            reply = msg.make_reply()

            if ';' not in msg.body:
                reply.body = "I don't understand you. Please send message with format:\n<topic>;<topic-keyword> <topic-keyword>..."
                await self.send(reply)
            else:
                try:
                    places = self.message_parse(msg.body)
                except IndexError:
                    print("")
                finally:
                    lookup = LookUpBehaviour((reply, places))
                    self.agent.add_behaviour(lookup) # FIXME placeholder add msg template
        else:
            print(f'{self.__class__.__name__}: no messages in 10 sec')
        if self.get('stop'):
            self.agent.stop()

    def message_parse(self, text):
        splitstr = text.split(';')
        # places = []
        # for i in range(len(splitstr) // 2):
        #     if splitstr[2*i]:
        #         places.append({"place": splitstr[2 * i], "keywords": splitstr[2 * i + 1].split(',')})
        keywords = []
        if len(splitstr) > 1:
            keywords = [keyword for keyword in splitstr[1].split(" ") if keyword]
        places = {'place':splitstr[0], 'keywords':keywords}
        print(f"Parsed message with params: {places}")
        return places



class LookUpAgent(Agent):
    async def setup(self):
        print(f'{self.__class__} started')
        b = AwaitRequestBehaviour()
        template = Template()
        self.add_behaviour(b)#, template)


