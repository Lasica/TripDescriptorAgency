from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.template import Template
from spade.message import Message


# class LookUpBehaviour(OneShotBehaviour):
        # print(f'{self.__class__.__name__}: init')
    # def __init__(self, msg, topic, keywords, source='wikipedia'):
    #     super().__init__()
    #     self.topic = topic
    #     self.keywords = keywords
    #     self.source = source
    #     self.reply = msg

    # async def run(self):
    #     print(f'{self.__class__.__name__}: running')
        # print(f'{self.__class__.__name__}: running')

        #TODO run summariser from access_web_resource
        # reply = self.get('reply')
        # reply.body = self.get('topic') + ': ' + ', '.join(self.get('keywords'))


class AwaitRequestBehaviour(CyclicBehaviour):
    async def run(self):
        print(f'{self.__class__.__name__}: running')

        msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
        if msg:
            print(f'{self.__class__.__name__} Message received with content: {msg.body}')

            reply = msg.make_reply()

            if ';' not in msg.body:
                reply.body = "I don't understand you. Please send message with format:\n<topic>;<topic-keyword>,<topic-keyword>;<next-topic>..."
                await self.send(reply)
            else:
                places = self.message_parse(msg.body)
                for entry in places:
                    # lookup = LookUpBehaviour()
                    # lookup.set('topic', entry['place'])
                    # lookup.set('keywords', entry['keywords'])
                    # lookup.set('reply', reply)
                    # #self.agent.add_behaviour(lookup) # FIXME placeholder add msg template
                    # lookup.set_agent(self.agent)
                    # await lookup.start()
                    topic = entry['place']
                    keywords = entry['keywords']
                    reply = self.get('reply')
                    reply.body = topic + ': ' + ', '.join(keywords)

                    await self.send(reply)

            #await self.agent.stop()
        else:
            print(f'{self.__class__.__name__}: no messages in 10 sec')

    def message_parse(self, text):
        # TODO write tests for this function
        splitstr = text.split(';')
        places = []
        for i in range(len(places) // 2):
            if splitstr[2*i]:
                places[i] = {"place": splitstr[2 * i], "keywords": splitstr[2 * i + 1].split(',')}
        return places


class LookUpAgent(Agent):
    async def setup(self):
        print(f'{self.__class__} started')
        b = AwaitRequestBehaviour()
        template = Template()
        self.add_behaviour(b)#, template)

