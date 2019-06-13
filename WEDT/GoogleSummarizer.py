from urllib import request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import nltk
import re
import heapq

# kroki w wydobyciu informacji z tekstu to po kolei
# uzyskanie czystego tekstu (bez htmlów etc): wykonywane przez request.urlopen().read().decode()
#   a następnie przez użycie beatifulSoup do wyciągnięcia tekstu z htmlu (piękna zupa to biblioteka do wyciągania tekstu
#   z htmlu i xmlu
# podział tekstu na zdania: nltk.sent_tokenize()
# podział zdań na tokeny: nltk.word_tokenize()
# przypisanie do zdań tagów części mowy: nltk.post_tag
# wykrycie entities (entity detection)
# wyszukiwanie relacji między entities w tekście

#alternatywne podejście na tę chwilę jeszcze, to zrobienie samego podsumowania tekstu poprzez wyszukanie zdań zawierających
#słowa, które najczęściej będą się powtarzać (czyt. najbardziej podsumowują tekst).
#udało mi się to zaimplementować, jednakże można to poprawić: niekiedy zwraca zdania w trochę złej kolejności:
#oczywista heurystyka w wypadku wikipedii i ogólnie tekstów opisowych turystycznych może działać na zasadzie
#Pobierz pierwsze kilka zdań bo zwykle w nich jest zawarty konkret, a później dopasuj pozostałe. do rozważenia
class GoogleSummarizer:
    def __init__(self, sentence_length, summary_length, keywords_weight, keywords):
        self.sent_lent    = sentence_length #maksymalna długość zdania które chcemy mieć w podsumowaniu
        self.sum_len      = summary_length #liczba zdań które chcemy mieć w podsumowaniu
        self.summary_list = {} #słownik podsumowań do robienia podsumowania z podsumowań
        self.keywords     = keywords
        self.keywords_weight = keywords_weight

    def summarize_web_sources(self, url):
        for i in url:
            try:
                req  = Request(i, headers={'User-Agent': 'Mozilla/5.0'})
                #html = request.urlopen(i).read().decode('utf8')
                html =  urlopen(req).read().decode('utf8')
            except:
                return "ERROR"

            raw = BeautifulSoup(html, 'html.parser')


            if ('wikipedia' in i):
                raw = self.preprocess_wiki_text(raw)#w tym momencie raw powinien zawierać normalny tekst z danej strony
            else:
                raw = self.paragraphize(raw)
                #raw = raw.get_text()#jeśli tekst nie jest z wiki, to nie musimy go dodatkowo przetwarzać
            # z kolei w formatted_text usunięto znaki specjalne i cyfry, jest przydatny do badania częstotliwości wyrazów,
            # z raw skorzystamy do zbudowania podsumowania
            formatted_text = self.preprocess_format_summary(raw)
            summary = self.create_summary(raw, self.words_weighted_frequencies(formatted_text))
            return(summary)
            #self.summary_list.append(summary)
    #wyszukanie paragrafów
    def paragraphize(self, text):
        paragraphs = text.find_all('p')
        article = ''

        for p in paragraphs:
            article += p.text
        return article

    def summarize_text(self, text):
        # z kolei w formatted_text usunięto znaki specjalne i cyfry, jest przydatny do badania częstotliwości wyrazów,
        # z raw skorzystamy do zbudowania podsumowania
        formatted_text = self.preprocess_format_summary(text)
        summary = self.create_summary(text, self.words_weighted_frequencies(formatted_text))
        return(summary)


    #wyszukanie paragrafów
    def paragraphize(self, text):
        paragraphs = text.find_all('p')
        article = ''

        for p in paragraphs:
            article += p.text
        return article

    #usuwanie znaków specjalnych oraz cyfr
    def preprocess_format_summary(self, text):
        formatted_article_text = re.sub('[^\'a-zA-Z]', ' ', text)
        formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
        return formatted_article_text

    # funkcja do tworzenia podsumowania
    def create_summary(self, text, word_frequencies):
        sentences = nltk.sent_tokenize(text)

        sentence_scores = {}
        for i in range(0, len(sentences)):
            for word in nltk.word_tokenize(sentences[i].lower()):
                if word in word_frequencies.keys():
                    if len(sentences[i].split(' ')) < self.sent_lent:
                        if i not in sentence_scores.keys():
                            sentence_scores[i] = word_frequencies[word]
                        else:
                            sentence_scores[i] += word_frequencies[word]
        summary_sent_id = heapq.nlargest(self.sum_len, sentence_scores, key=sentence_scores.get)
        if 0 not in summary_sent_id:
            summary_sent_id.append(0)#heurystyka: zakładamy, że pierwsze zdanie ma jakieś dobre podsumowanie tematu
            #może dodać dodatkowe warunki aby łapać zdania mimo wszystko, a nie jakieś legendy map albo zawartości tabelajek
        summary_sent_id.sort()#porządkujemy indeksy
        summary_sent = [sentences[i] for i in summary_sent_id]
        summary = ' '.join(summary_sent)
        return summary

    # funkcja do wyliczania częstotliwości słów
    def words_weighted_frequencies(self, formatted_text):
        stopwords = nltk.corpus.stopwords.words('english')

        word_frequencies = {}
        for word in nltk.word_tokenize(formatted_text):
            if word not in stopwords:
                word_frequencies[word] = word_frequencies.get(word, 0) + 1
        maximum_freq = max(word_frequencies.values())

        for word in word_frequencies.keys():
            word_frequencies[word] /= maximum_freq
            if word in self.keywords:
                word_frequencies[word] *= self.keywords_weight # TODO remove magic numbers
        return word_frequencies

    #metoda specjalnie na przyszykowanie tekstu z wikipedii
    def preprocess_wiki_text(self, document):
        article = self.paragraphize(document)

        #usunięcie odnośników wikipedii
        article = re.sub(r'\[[0-9]*\]', ' ', article)
        article_text = re.sub(r'\s+', ' ', article)
        #usunięcie odnośników wikipedii

        return article



#summary = Summarizer(30, 10)
#summary.summarize_web_sources(gs.Gsearch())
