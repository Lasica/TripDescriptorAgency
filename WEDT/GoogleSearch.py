from googlesearch import search

class GoogleSearch:
    def __init__(self, name_search):
        self.name = name_search
        self.urls = []

    def Gsearch(self):
        res_num = 0

        for i in search(query=self.name, tld='co.in', lang='en',num=1, stop=1, pause=2):#zdefiniować parametry wyszukania jako zmienne klasy
            res_num += 1
            print (res_num)
            print(i + '\n')
            self.urls.append(i)
        return self.urls
#gs = GoogleSearch('Poland ')
