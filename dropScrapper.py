from bs4 import BeautifulSoup
from pandas import DataFrame
import requests
import re


def getSoup(url, header):
    response = requests.get(url, headers=header)
    return BeautifulSoup(response.text, "html.parser")

def nikeScrapper():
    url = 'https://www.nike.com/launch?s=upcoming'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    drop = dict()
    for i in soup.findAll('a'):
        temp = str(i)
        if 'product-card-link' in temp:
            # print(temp)
            name = re.search(r'aria-label="(.*?)"',temp).group(1)
            mon = re.search(r'"test-startDate">(.*?)<',temp).group(1)
            day = re.search(r'"test-day">(.*?)<',temp).group(1)
            # print(name)
            drop[name] = (mon,day)
    return drop

## adidas hides the date of products between strong > ... <
## this means when you search for it it doesnt show up
## a work around could be to go to every link and grab from there

# def adidasScrapper():
#     url = 'https://www.adidas.com/us/release-dates'
#     header = {
#         'User-Agent': 'My User Agent 1.0',
#         'From': 'youremail@domain.com'
#     }
#     soup = getSoup(url, header)
#     drop = dict()
#     for i in soup.findAll('div'):
#         if 'strong' in str(i):
#             print(i)
#         # if 'plc-products' in i:
#         #     temp = str(i)
#         #     print(temp)

def exportExcel():
    nike = nikeScrapper()
    name = []
    time = []
    for i in nike:
        name.append(i)
        tformat = "{} {}".format(nike[i][0], nike[i][1])
        time.append(tformat)
    df = DataFrame({'Name': name, 'Drop Time': time})
    df.to_excel('DropList.xlsx', sheet_name = 'Nike', index = False)

exportExcel()
