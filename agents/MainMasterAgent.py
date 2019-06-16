from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template
import time
import uuid

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
    def __init__(self, task):
        super().__init__()
        self.result = None
        self.error = None
        self.task = task

    async def run(self):
        print(f'{self.__class__.__name__}: running {self.task}')
        request = Message(to=self.template.sender, thread=self.template.thread)
        request.body = self.task
        await self.send(request)
        response = await self.receive(timeout=360)
        if response:
            self.result = response.body
        else:
            self.error = True


class ClientDialogueBehaviour(CyclicBehaviour):
    def __init__(self, msg):
        super().__init__()
        self.reply_template = msg.make_reply()
        self.first_message = msg
        self.jobs = []

    async def on_start(self):
        self.reply_template.body = helloMessage
        await self.send(self.reply_template)

    async def run(self):
        print(f'{self.__class__.__name__}: running')
        request = await self.receive(timeout=360)
        print(f'{self.__class__.__name__}: received message {request}')
        if request and "finish" not in request.body:
            if ";" in request.body:
                self.reply_template.body = "Acknowledged. I'm ready for further instructions."
                await self.send(self.reply_template)

                for job, address in addressBook.items():
                    t = Template(sender=address, thread=uuid.uuid4())
                    self.agent.add_behaviour(self.jobs[-1], t)
                    self.jobs.append(QuerryForInfoBehaviour(request.body))
            else:
                self.reply_template.body = "The pattern is wrong. Use: <topic>; <optional: keywords>"
                await self.send(self.reply_template)
        else:
            self.kill()

    async def on_end(self):
        self.reply_template.body = finishMessage.format(self.compile_answer())
        await self.send(self.reply_template)

    def compile_answer(self):
        tries = 10
        while tries > 1:
            finished = all([beh.is_done() for beh in self.jobs])
            if finished:
                break
            self.reply_template.body = f"Collecting necessary information... {10-tries}"
            self.send(self.reply_template)
            time.sleep(5)
            tries -= 1
        resultsFromBehs = [beh.result for beh in self.jobs if beh.is_done() and not beh.error]
        return "\n---\n".join(resultsFromBehs)


class MainMasterBehav(CyclicBehaviour):
    async def run(self):
        results = {}
        print(f'{self.__class__.__name__}: running')

        request = await self.receive()
        print(f'{self.__class__.__name__}: received message {request}')

        if request:
            cb = ClientDialogueBehaviour(request)
            self.agent.add_behaviour(cb, Template(sender=request.sender))
            await cb.enqueue(request)


class MainMasterAgent(Agent):
    async def setup(self):
        print(f'{self.__class__.__name__} started')
        b = MainMasterBehav()
        templates = [Template(sender=address) for address in addressBook.values()]
        template = templates[0]
        for t in templates:
            template = template | t
        self.add_behaviour(b, ~template)


