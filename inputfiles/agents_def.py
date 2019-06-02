import time
from spade.agent import Agent
from spade.message import Message
from spade.template import Template
from spade import quit_spade
from spade.behaviour import CyclicBehaviour
from access_web_resource import Summarizer
from access_web_resource import GoogleSearch

#główny agent rozsyłający żądania
class MainControlAgent(Agent):
    pass
# główny agent rozsyłający żądania

# wysłanie żądania plus składanie/selekcja tekstów per lokacja w całość
# zachowania
# czekanie na wezwanie od głównego kontrolera i wysłanie wiadomości
# czekanie na podsumowanie z konkretnego źródła i odłożenie go gdzieś
# sprawdzanie czy wszystkie podsumowania są zebrane oraz ich złożenie i przesłanie wyżej
class  PlacesAgent(Agent):
    class ReqProcessBehaviour(CyclicBehaviour):
        async def run(self):
            print("Request received")

            msg = await self.receive(timeout=10) # wait for a message for 10 seconds
            if msg:
                print("Message received with content: {}".format(msg.body))

            # stop agent from behaviour
            await self.agent.stop()

# pojedynczy agent wykonujący przeszukanie oraz podsumowanie w jednym źródle
# pobiera dane, robi wyszukanie, wywołuje funkcję do podsumowania i je zwraca
class SummarizerAgent(Agent):
    pass