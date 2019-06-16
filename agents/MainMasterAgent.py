from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template

addressBook = {
    "place": "PlacesMaster@blabber.im",
    #"food": "",
    #"sleep": ""
}


helloMessage = "Hello, I am Trip Descriptor Agent. Message me a list of places you would like to visit and keywords " \
               "that highlight what you would like to see there and I can make description of such trip for you." \
               "Say finished when you are finished. Example of the request:\n Warsaw; palace of culture\n" \
               "Warsaw; museum of warsaw uprising\nfinished"
finishMessage = "Here's what I've been able to compose so far:\n{}"

class QuerryForInfoBehaviour(OneShotBehaviour):
    def __init__(self, origin):
        super().__init__()
        self.result = None

    async def run(self):
        print(f'{self.__class__.__name__}: running {self.origin}')



class ClientDialogueBehaviour(CyclicBehaviour):
    def __init__(self, msg):
        super().__init__()
        self.reply_template = msg.make_reply()
        self.first_message = msg
        self.jobs = []

    async def gather_info(self, topic, keywords):
        # ask all of your sources for given topic with keywords
        for contact, address in addressBook.items():
            msg = Message(to=address)
            # msg.set_metadata(contact, "request")
            # msg.body = request.body
            # await self.send(msg)

    async def on_start(self):
        self.reply_template.body = helloMessage
        await self.send(self.reply_template)

    async def run(self):
        print(f'{self.__class__.__name__}: running')
        request = await self.receive(timeout=360)
        if request and "finish" not in request.body:
            if ";" in request.body:
                self.reply_template.body = "Acknowledged. I'm ready for further instructions."
                await self.send(self.reply_template)

                self.jobs.append(QuerryForInfoBehaviour)
            else:
                self.reply_template.body = "The pattern is wrong. Use: <topic>; <optional: keywords>"
                await self.send(self.reply_template)
        else:
            self.reply_template.body = finishMessage.format(self.compile_answer())
            await self.send(self.reply_template)
            self.kill()

        #
        # for i in range(len(addressBook)):
        #     result = await self.receive()
        #     results[result.sender] = result.body
        #
        # response = Message(to=request.sender)
        # response.body = "\n".join(results.values())
        # await self.send(response)



class MainMasterBehav(CyclicBehaviour):
    async def run(self):
        results = {}
        print(f'{self.__class__.__name__}: running')

        request = await self.receive()

        if request:
            reply = request.make_reply()
            # reply.body = helloMessage
            # await self.send(reply)
            cb = ClientDialogueBehaviour(request)
            self.agent.add_behaviour(cb, Template(sender=request.sender))

            # for contact, address in addressBook.items():
            #     msg = Message(to=address)
            #     msg.set_metadata(contact, "request")
            #     msg.body = request.body
            #     await self.send(msg)
            #
            # response = Message(to=request.sender)
            # response.body = "\n".join(results.values())
            # await self.send(response)


class MainMasterAgent(Agent):
    async def setup(self):
        print(f'{self.__class__.__name__} started')
        b = MainMasterBehav()
        templates = [Template(sender=address) for address in addressBook.values()]
        template = templates[0]
        for t in templates:
            template = template | t
        self.add_behaviour(b, ~template)


