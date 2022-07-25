import requests
from bs4 import BeautifulSoup
import json

class Soupify:
    """docstring for Soupify"""
    def __init__(self):
        
        self.page = "https://www.olx.pl"

    def _connect(self):
        
        try:
            page = requests.get(self.page)
            return page
        except Exception as e:
            raise e


    def _beautify(self):
        con = self._connect()
        data = BeautifulSoup(con.content, 'html.parser')
        return data

    def load_data(self):


        data = self._beautify()

        parent = data.find(id="gallerywide")
       
        children = parent.find_all("li")

        res = []

        for l in children:
            
            li_dict = dict()
            if l.find('a') is None:
                continue
            title_encode = l.find('a')['title'].encode("ascii", "ignore")
            title = title_encode.decode()
            li_dict['title'] = title
           
            
            des_html = l.find('strong').get_text().encode("ascii", "ignore")
            description = des_html.decode()
            li_dict['description'] = description
            # li_dict['description'] = str(l.find('ul', attrs={'class': 'date-location'}))

            # Some prices are in text, this was not handled as I do not understand the language
            price_div = l.find('div', attrs={'class': 'price'}).get_text()
            price_item = [s for s in price_div.split() if s.isdigit()]
            price = "".join(price_item)
            li_dict['price'] = float(price) if price else None

            img_tag = l.find('img')
            li_dict["image"] = img_tag['src']

            res.append(li_dict)

        print("loading data........")
        # print(res)
        return res



class JsonWrite:

    def __init__(self, data):
        self.data = data

    def write(self):
        try:
            jsonString = json.dumps(self.data)
            jsonFile = open("data.json", "w")
            print("writing to json file.........")
            jsonFile.write(jsonString)
            jsonFile.close()
            print("Done")
        except Exception as e:
            print(f"Cannot write to file {e}")
            raise e


if __name__ == '__main__':
    soup = Soupify()
    data = soup.load_data()

    load_json = JsonWrite(data)
    load_json.write()






