from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template

addressBook = {
    "wikipedia": "LookUpAgent2@blabber.im",
    "wikitravel": 'LookUpAgent1@blabber.im',
    "google": "LookUpAgent3@blabber.im"
}




class ClientDialogueBehaviour(OneShotBehaviour):
    def __init__(self, msg):
        super().__init__()
        self.reply_template = msg.make_reply()
        self.first_message = msg

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

        #
        # for i in range(len(addressBook)):
        #     result = await self.receive()
        #     results[result.sender] = result.body
        #
        # response = Message(to=request.sender)
        # response.body = "\n".join(results.values())
        # await self.send(response)


class MainPlacesBehaviour(CyclicBehaviour):
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
            # for i in range(len(addressBook)):
            #     result = await self.receive()
            #     results[result.sender] = result.body
            #
            # response = Message(to=request.sender)
            # response.body = "\n".join(results.values())
            # await self.send(response)


class PlacesAgent(Agent):
    async def setup(self):
        print(f'{self.__class__.__name__} started')
        b = MainPlacesBehaviour()
        templates = [Template(sender=address) for address in addressBook.values()]
        template = templates[0]
        for t in templates:
            template = template | t
        self.add_behaviour(b, ~template)


