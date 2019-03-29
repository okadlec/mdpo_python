from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

nemocniceUrl = 'http://elp.mdpo.cz/ElpDepartures/Home/Departures?stop=10'
englisovaUrl = 'http://elp.mdpo.cz/ElpDepartures/Home/Departures?stop=12'

def zmena_textu( text ):
    text = text.replace(',','')
    text = text.replace(',','')
    text = text.replace('ě','e')
    text = text.replace('š','s')
    text = text.replace('č','c')
    text = text.replace('ř','r')
    text = text.replace('ž','z')
    text = text.replace('ý','y')
    text = text.replace('á','a')
    text = text.replace('í','i')
    text = text.replace('é','e')
    text = text.replace('ů','u')
    text = text.replace('ú','u')
    return text

# připojuje se a a bere stranku
uClient = uReq(nemocniceUrl)
# uklada si stranku
pageHtml = uClient.read()
# odpojuje se
uClient.close
# html parser
pageSoup = soup(pageHtml,"html.parser")
# vezme všechny divy v textu
elpText = pageSoup.find("div",{"class":"elpText"})
# list divu
divsNemocnice = elpText.findAll("div")
# list stanic
containersNemocnice = elpText.findAll("div",{"class":"stationNameBox"})

# připojuje se a a bere stranku
uClient = uReq(englisovaUrl)
# uklada si stranku
pageHtml = uClient.read()
# odpojuje se
uClient.close
# html parser
pageSoup = soup(pageHtml,"html.parser")
# vezme všechny divy v textu
elpText = pageSoup.find("div",{"class":"elpText"})
# list divu
divsEnglisova = elpText.findAll("div")
# list stanic
containersEnglisova = elpText.findAll("div",{"class":"stationNameBox"})

filename = r'C:\Users\vines\Desktop\db.json'
f = open(filename,"w")

headerNemocnice = '{\n"Nemocnice":{'
f.write(headerNemocnice)

# Vypiše všechny linky z nemocnice směr do centra
num = 0;
pom = 0;
for container in containersNemocnice:
    if (container.text == "Kateřinky" or container.text == "Globus" or container.text == "Kylešovice, Bílovecká") and pom < 2:
        if pom == 0:
            cislo = divsNemocnice[0+4*num].text
            smer = divsNemocnice[1+4*num].text
            smer = zmena_textu(smer)
            odjezd = divsNemocnice[3+4*num].text
            print(cislo)
            print(smer)
            print(odjezd)        
            print("-------------") 
        if pom == 1:
            dalsi_cislo = divsNemocnice[0+4*num].text
            dalsi_smer = divsNemocnice[1+4*num].text
            dalsi_smer = zmena_textu(dalsi_smer)
            dalsi_odjezd = divsNemocnice[3+4*num].text 
            print(dalsi_cislo)
            print(dalsi_smer)
            print(dalsi_odjezd)
            print("-------------")  
        pom += 1
    num += 1
f.write('"number":'+ cislo + ', "direction": "' + smer + '", "departure":"' + odjezd + '", "next_number":' + dalsi_cislo + ', "next_direction": "' + dalsi_smer + '", "next_departure":"' + dalsi_odjezd + '"},')

headerEngl = '\n"englisova":{'
f.write(headerEngl)

num = 0;
pom = 0;
for container in containersEnglisova:
    if (container.text == "Kateřinky") and pom < 2:
        if pom == 0:
            cislo = divsEnglisova[0+4*num].text
            smer = divsEnglisova[1+4*num].text
            smer = zmena_textu(smer)
            odjezd = divsEnglisova[3+4*num].text
            print(cislo)
            print(smer)
            print(odjezd)        
            print("-------------") 
        if pom == 1:
            dalsi_cislo = divsEnglisova[0+4*num].text
            dalsi_smer = divsEnglisova[1+4*num].text
            dalsi_smer = zmena_textu(dalsi_smer)
            dalsi_odjezd = divsEnglisova[3+4*num].text 
            print(dalsi_cislo)
            print(dalsi_smer)
            print(dalsi_odjezd) 
        pom += 1
    num += 1
f.write('"number":'+ cislo + ', "direction": "' + smer + '", "departure":"' + odjezd + '", "next_number":' + dalsi_cislo + ', "next_direction": "' + dalsi_smer + '", "next_departure":"' + dalsi_odjezd + '"}')
f.write('\n}')
f.close()
