from urllib import request
from bs4    import BeautifulSoup
import nltk
import re
import pprint
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
class Summarizer:
    def __init__(self, sentence_length, summary_length):
        self.sent_lent    = sentence_length #maksymalna długość zdania które chcemy mieć w podsumowaniu
        self.sum_len      = summary_length #liczba zdań które chcemy mieć w podsumowaniu
        self.summary_list = {} #słownik podsumowań do robienia podsumowania z podsumowań

    def summarize_web_sources(self, url):
        for i in url:
            html = request.urlopen(i).read().decode('utf8')
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
            print(summary)
            self.summary_list.append(summary)
    #wyszukanie paragrafów
    def paragraphize(self, text):
        paragraphs = text.find_all('p')
        article = ''

        for p in paragraphs:
            article += p.text
        return article

    #usuwanie znaków specjalnych oraz cyfr
    def preprocess_format_summary(self, text):


        formatted_article_text = re.sub('[^a-zA-Z]', ' ', text)
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
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1
        maximum_freq = max(word_frequencies.values())

        for word in word_frequencies.keys():
            word_frequencies[word] = word_frequencies[word] / maximum_freq
        return word_frequencies

    #metoda specjalnie na przyszykowanie tekstu z wikipedii
    def preprocess_wiki_text(self, document):
        article = self.paragraphize(document)

        #usunięcie odnośników wikipedii
        article = re.sub(r'\[[0-9]*\]', ' ', article)
        article_text = re.sub(r'\s+', ' ', article)
        #usunięcie odnośników wikipedii

        return article


def build_chunked_tree(tagged_sentences, grammar):#budowa drzewek dla listy zdań
    pass

def chunk_sentences(tagged_sentence, grammar):
    chunk_rules = nltk.RegexpParser(grammar)#tworzenie drzewa zdania, definujemy parser
    return chunk_rules.parse(tagged_sentence)

def vocab_build(text):
    tokens = nltk.wordpunct_tokenize(text)
    #wybór interesujących tokenów, dodać może jakąś funkcję do zrobienia tego
    text = nltk.Text(tokens)
    words = [w.lower() for w in text]
    return sorted(set(words))

def preprocess_doc(document):
    sentences   = nltk.sent_tokenize(document)#podział na zdania
    token_sent  = [nltk.word_tokenize(sent) for sent in sentences]#tokenizacja zdań
    pos_sent    = [nltk.pos_tag(tok_sent) for tok_sent in token_sent]#przypisanie części mowy wyrazom w zdaniu
    return pos_sent

class GoogleSearch:
    def __init__(self, name_search):
        self.name = name_search
        self.urls = []

    def Gsearch(self):
        res_num = 0
        try:
            from googlesearch import search
        except ImportError:
            print("No Module named 'google' Found")
        for i in search(query=self.name, tld='co.in', lang='en',num=10,stop=1,pause=2):#zdefiniować parametry wyszukania jako zmienne klasy
            res_num += 1
            print (res_num)
            print(i + '\n')
            self.urls.append(i)
        return self.urls

gs = GoogleSearch('Poland ')
summary = Summarizer(30, 10)
summary.access_web_resource(gs.Gsearch())
