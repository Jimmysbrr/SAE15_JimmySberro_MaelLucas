import requests
from lxml import etree
import os
import time
from datetime import datetime
import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from math import sqrt


################################################################################################################################################################

"""Tutoriel d'utilisation

Executer le programme python dans le terminal pour assurer la création des repertoire au bon chemin
ensuite lors de l'execution suivre les instructions

-le repertoire data-xml contient tout les document crée lors des capture (pour l'analyse des capture c'est le nom du fichier se trouvant ici qu'il faut donner il est recommander de renommer les analyses faites)
-le repertoire xml-request-log contient la dernier requete brut en cas de debuggage

les analyses et capture json ne sont malheuresement pas encore fonctionnel donc peut mettre fin au programme si séléctionné"""


################################################################################################################################################################

def check_existing_files_or_create(name):
    path = str(os.getcwd())+"/"+name          #cette fonction permet de verifiér l'existance d'un repertoire et sinon le crée
    print(path)
    chk = os.path.exists(path)
    if chk == True:
        print("")
        return(path)
    else:
        os.mkdir(path)
        print("le fichier", name,"a été ajouter au repertoire courant")
        return(path)

#envoye la requete http vers le site d'un parking "nom" et revoye le contenue xml de la page
def xml_request(nom):
    parking_request = str("https://data.montpellier3m.fr/sites/default/files/ressources/"+nom+".xml") 
    data = requests.get(parking_request)
    return(data)
"""
def json_request():
    json_request1 =  "https://montpellier-fr-smoove.klervi.net/gbfs/en/station_information.json"
    json_request2 = "https://montpellier-fr-smoove.klervi.net/gbfs/en/station_status.json"
    data = requests.get(json_request1)
    data2 = requests.get(json_request2)
    path= check_existing_files_or_create("data-json")
    print(data.text,data2.text)
    return(data,data2)
json_request()"""

#print les données xml
def show_xml(xml_data):
    print(xml_data.text)

#programme principale
def data_scrap(time_total,time_request):
    time_today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_start = time.time()
    time_set = time.time()

    path= check_existing_files_or_create("data-xml")
    path2= check_existing_files_or_create("xml-request-log")
    parking=['FR_MTP_ANTI','FR_MTP_COME','FR_MTP_CORU','FR_MTP_EURO','FR_MTP_FOCH','FR_MTP_GAMB','FR_MTP_GARE','FR_MTP_TRIA','FR_MTP_ARCT',
    'FR_MTP_PITO','FR_MTP_CIRCE','FR_MTP_SABI','FR_MTP_GARC','FR_MTP_SABL','FR_MTP_MOSS','FR_STJ_SJLC','FR_MTP_MEDC',
    'FR_MTP_OCCI','FR_MTP_GA109','FR_MTP_GA250','FR_CAS_CDGA','FR_MTP_POLY']

    while time_start + time_total > time_set :
        for i in parking:
            parking_request = str("https://data.montpellier3m.fr/sites/default/files/ressources/"+i+".xml") 
            data = requests.get(parking_request)
            os.chdir(path2)
            fichier = open("xml-log", "w", encoding="utf-8") #contient juste le code xml
            fichier.write(data.text)
            fichier.close()
            tree = etree.parse("xml-log") 
            os.chdir(path)
            fichier2 = open(time_today, "a", encoding="utf-8") #contient les données importante !!!

            for user in tree.xpath("Free"):
                fichier2.write(user.text)
                print(user.text)
                fichier2.write("\n")

            for user in tree.xpath("Total"):        ####creation et remplissage des fichier avec les data de la page xml pour chaques parkings####
                fichier2.write(user.text)
                print(user.text)
                fichier2.write("\n")

            for user in tree.xpath("Name"):
                fichier2.write(user.text)
                print(user.text)
                print("\n")
                fichier2.write("\n")
                fichier2.write("\n")

            fichier2.close()
        fichier2 = open(time_today, "a", encoding="utf-8")
        fichier2.write("f")
        fichier2.close()

        print("Prochaine requete dans ",time_request," secondes ...")
        time.sleep(time_request)
        time_set = time.time()
        os.system("clear")

def recuperation_velo():
    path = check_existing_files_or_create("data-json")
    temp = 0
    nom = []
    id = []
    dispo_velo =[]
    dispo_borne = []
    time_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_each = int(input("temps entre chaques captures (en secondes) ? : \n"))
    time_total = int(input("temps total de capture (en secondes) ? : \n"))
    temps = [0]
    time_list = 0
    time_set = 0
    temps_tool = time.time()
    velo_list=[]
    moyenne = 0
    moyenne_list = []
    min = 0
    sigma = 0
    capacite = []
    while temps_tool + time_total > time_set :
        requete1 = requests.get("https://montpellier-fr-smoove.klervi.net/gbfs/en/station_information.json")
        data1 = requete1.json()
        requete2 = requests.get("https://montpellier-fr-smoove.klervi.net/gbfs/en/station_status.json")
        data2 = requete2.json()
        
        for i in data1["data"]["stations"]:
            id.append(i["station_id"])
            capacite.append(i["capacity"])
            nom.append(i["name"])
        
        for x in data2["data"]["stations"]:
            dispo_velo.append(x["num_bikes_available"])
            dispo_borne.append(x["num_docks_available"])
        for z in dispo_borne:
            moyenne += z
            print(moyenne)
        moyenne = moyenne // len(dispo_borne)
        moyenne_list.append(moyenne)
        time_set = time.time()
        time.sleep(time_each)
        moyenne = 0
        print(dispo_borne)
        dispo_borne = []

    for i in range(len(moyenne_list)-1):
        time_list+=time_each
        temps.append(time_list)
    min = moyenne_list[0]

    max = moyenne_list[0]
    
    for i in moyenne_list:
        moyenne += i
    moyenne = moyenne//len(moyenne_list)
    sigma = 0
    for i in moyenne_list:
        sigma += (i - moyenne)**2
    sigma = sqrt(sigma)//len(moyenne_list)

    
    print("ecart type :",sigma)
    os.chdir(path)
    fichier = open(time_start, "a", encoding= "utf-8")
    for i in moyenne_list:
        fichier.write(i)
        fichier.write("\n")
    fichier.write("sigma =")
    fichier.write(sigma)
    fichier.close()
    plt.plot(temps,moyenne_list)
    plt.plot(sigma)
    liste_velo = []
    plt.xlabel("temps en minutes")   
    plt.ylabel("place libre")
    plt.show()

def analyse_velo():
    path = check_existing_files_or_create("data-json")   #chemin de teste 2023-01-21 09:10:15
    choix3 = input("titre du fichier a lire et analyser? :\n")
    choix4 = input("durée entre chaques requete de la capture ? (en minutes)\n")
    time.sleep(0.5)
    os.chdir(path)
    f1 = open(choix3, "r", encoding="utf-8") #contient juste le code xml
    lecture = f1.read()
    nb_request = 0
    read_element = []
    element = ["",""]
    table_velo = []
    count = 0
    temp = ""
    sigma = ""
    for i in lecture:
        if i == "\n" and count == 0:
            table_velo.append(int(temp))
        elif i == "=":
            count = 1
        if i != "\n" and i.isdigit() == True:
            temp += i
        if i != "\n" and count == 1 and i.isdigit() == True:
            sigma += i


        



def menu_main():
    os.system("clear")
    print("----------------------------------------")
    print("|           Data_xml_MTP V1.0          |")
    print("|           SAE 15 : Données           |")
    print("----------------------------------------\n")
    time.sleep(1)
    choix1 = input("analyse / capture (a/c)\n")
    return(choix1)

def menu_capture():
    os.system("clear")
    print("----------------------------------------")
    print("|           Data_xml_MTP V1.0          |")
    print("|           SAE 15 : Données           |")
    print("|             Capture mode             |")
    print("----------------------------------------\n")
    time.sleep(0.5)
    input3 = input("capture velo ou parking ? (v/p)\n")
    if input3 == "p":
        input1 = input("temps de capture ? (en secondes) :\n")
        input2 = input("temps entre chaques requets ? (en secondes) :\n")
        return(data_scrap(int(input1),int(input2)))
    elif input3 == "v":
        return("v")
    
    

def menu_lecture2():
    os.system("clear")
    print("----------------------------------------")
    print("|           Data_xml_MTP V1.0          |")
    print("|           SAE 15 : Données           |")
    print("|             Analyse mode             |")
    print("----------------------------------------\n")
    time.sleep(0.5)
    input1 = input("format analyse ? (json / xml) :\n")
    return(input1)


def menu_lecture3():
    os.system("clear")
    print("----------------------------------------")
    print("|           Data_xml_MTP V1.0          |")
    print("|           SAE 15 : Données           |")
    print("|             Analyse mode             |")
    print("----------------------------------------\n")
    time.sleep(0.5)
    input1 = ("\n")
    return(input1)




def menu_lecture():
    os.system("clear")
    print("----------------------------------------")
    print("|           Data_xml_MTP V1.0          |")
    print("|           SAE 15 : Données           |")
    print("|             Analyse mode             |")
    print("----------------------------------------\n")
    time.sleep(0.5)
    path = check_existing_files_or_create("data-xml")   #chemin de teste 2023-01-21 09:10:15
    choix3 = input("titre du fichier a lire et analyser? :\n")
    choix4 = input("durée entre chaques requete de la capture ? (en minutes)\n")
    time.sleep(0.5)
    os.chdir(path)
    f1 = open(choix3, "r", encoding="utf-8") #contient juste le code xml
    lecture = f1.read()
    nb_request = 0
    read_element = []
    element = ["",""]
    table_car = []
    for i in lecture:
        if i.isdigit() == True:
            element[0] = element[0] + i
        elif i == "\n" and element[0] != "":
            read_element.append(int(element[0]))
            element = ["",""]
        elif i == "f":
            table_car.append([])
            table_car[nb_request] = read_element
            read_element = []
            nb_request += 1
    parking=['FR_MTP_ANTI','FR_MTP_COME','FR_MTP_CORU','FR_MTP_EURO','FR_MTP_FOCH','FR_MTP_GAMB','FR_MTP_GARE','FR_MTP_TRIA','FR_MTP_ARCT',
    'FR_MTP_PITO','FR_MTP_CIRCE','FR_MTP_SABI','FR_MTP_GARC','FR_MTP_SABL','FR_MTP_MOSS','FR_STJ_SJLC','FR_MTP_MEDC',
    'FR_MTP_OCCI','FR_MTP_GA109','FR_MTP_GA250','FR_CAS_CDGA','FR_MTP_ARCE','FR_MTP_POLY']
    moyenne_data = []
    element = 0
    element2 = 0 
    data_place = 0
    pair_data = 0
    moyenne = 0
    for i in table_car:
        for x in i:
            if pair_data == 1:
                pair_data = 0
                element = (100*element)//x
                moyenne_data.append(element)
                element = 0
                data_place += 1

            else :
                pair_data = 1
                element = x
    os.system("clear")
    print("poucentage des parkings rempli a chaque requete\n")
    print(moyenne_data,"\n\n\n")
    moyenne_final = []
    element = 0
    data_place = 0
    for i in range(len(parking)):
        element = moyenne_data[i]
        for x in range((len(moyenne_data)//len(parking))-1):
            element += moyenne_data[(data_place + (len(parking)*x))]   ##### calcule de la moyenne total sur toute la duré de la capture #####
        element = element / (len(moyenne_data)//len(parking))
        moyenne_final.append(element)
        element = 0
        data_place += 1
    print("moyenne total pour chaque parking sur toute la durée de capture\n")
    print(moyenne_final,"\n")
    temps = 0
    temps_list = []
    list_requete = []
    temporaire = []
    for i in range((len(moyenne_data)//len(parking))):
        temps_list.append(temps)
        temps += int(choix4) 
    for i in range(len(parking)):
        for x in range((len(moyenne_data)//len(parking))):
            temporaire.append(moyenne_data[i+(len(parking)*x)])
        list_requete.append(temporaire)
        temporaire = []
    print(list_requete)
    count=0
    y_debug = 999
    print("\n\n\n\n")
    debug_list = []
    for i in list_requete:
        for y in i:

            if y != i[0]:
                y_debug = 1 ####verification des données eronnée####
        if y_debug == 1:
            debug_list.append(i)
            print(temps_list,i)
            plt.plot(temps_list,i, label=str(parking[count]))
            plt.xlabel("temps en minutes")     ####affichage de l'evolution des pourcentage de place prises pour chaque parking####
            plt.ylabel("pourcentage de place prise")
            count +=1
        else:
            count +=1
        y_debug = 0
    plt.legend()
    plt.show()
    print(i)
    moyenne=0
    moyenne_liste=[]
    y1 = debug_list[0]
    print(y1)
    for i in range(len(debug_list[0])):
        for z in range(len(debug_list)):
            moyenne += debug_list[z][i]
        moyenne = moyenne // len(debug_list[0])
        moyenne_liste.append(moyenne)
        moyenne = 0
    plt.plot(temps_list,moyenne_liste)
    plt.xlabel("temps en minutes")          ####affichage de l'evolution des pourcentage de place prises pour la moyenne de tout les parking a chaques requete####
    plt.ylabel("pourcentage de places prises moyen")
    plt.show()

################################################################################################################################################################

"""programe principal"""

################################################################################################################################################################


def __Principale__():
    temp = menu_main()
    if temp == "c":
        time.sleep(0.5)
        if menu_capture() == "v":
            recuperation_velo()

        
    elif temp == "a":
        time.sleep(0.5)
        if menu_lecture2() == "xml":
            time.sleep(0.5)
            menu_lecture()

    else:
        print("BAD_RESPONSE {'a' or 'c' expected} restart ....")
        time.sleep(2)
        __Principale__()


__Principale__()