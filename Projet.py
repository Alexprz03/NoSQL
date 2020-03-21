import requests #pip install requests
import json 
import os
from pymongo import MongoClient #pip install pymongo
from prettyprinter import pprint #pip install prettyprinter

#https://api.openweathermap.org/data/2.5/weather?q=Paris&units=metric&appid=6e158381daf9b4adb34ced017030f780

def register_data():
	api_key = '6e158381daf9b4adb34ced017030f780'
	file = open("Cities.txt", "r")
	data = []

	for new_city in file:
		new_city = new_city.rstrip()
		url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(new_city, api_key)
		res = requests.get(url).json()

		# "404", means city is not found 
		if res["cod"] != "404": 
			# recherche des données dans le package
			info = []
			info.append(res["name"])
			weather = res["weather"]
			info.append(weather[0]["main"])
			info.append(weather[0]["description"])

			main = res["main"]
			info.append(main["temp"])
			info.append(main["pressure"])
			info.append(main["humidity"])
			data.append(info)

		else:
			print("ERROR: url not found for " + new_city)
	file.close()
	return data

def insert_database(Cities):
	weather.delete_many({})
	for City in Cities:
		insert = {
			'City': City[0],
			'Weather': City[1],
			'Description': City[2],
			'Temp (°C)': City[3],
			'Pressure (hPa)': City[4],
			'Humidity (%)': City[5]
		}
		weather.insert_one(insert)

def requests_nosql():
	os.system("cls")
	mean = 0
	print("Choisir une requete :")
	print("1 - Ville ou il fait le plus chaud actuellement")
	print("2 - Les nième villes les moins humides")
	print("3 - Liste des villes ou il pleut")
	print("4 - Temperature moyenne (parmis les villes entrées)")
	print("5 - Effectuer un tri")
	print("6 - Rechercher les données d'une ville")

	c = input("Choix : ")

	if c == '1':
		var = weather.find().sort("Temp (°C)", -1).limit(1)
		for a in var:
			pprint(a)
	
	elif c == '2':
		n = int(input("Vous voulez obtenir les .. ème villes les moins humides\n"))
		var = weather.find().sort("Humidity (%)", 1).limit(n)
		for a in var:
			pprint(a)

	elif c == '3':
		var = weather.find({'Weather': 'Rain'}).sort("City", 1)
		for a in var:
			pprint(a)

	elif c == '4':
		cmpt = 0
		mean = 0
		var = weather.find()
		for a in var:
			mean = mean + a['Temp (°C)']
			cmpt = cmpt+1
		mean = round(mean/cmpt,2)
		print("La temperature moyenne est " + str(mean) + " °C")

	elif c == '5': #Tri
		print("\nChoisir ce que vous voulez trier")
		print("1 - Trier en fonction des noms (tri alphabetique)")
		print("2 - Trier en fonction du temps")
		print("3 - Trier en fonction de la temperature ")
		print("4 - Trier en fonction de la pression ")
		print("5 - Trier en fonction de l'humidité ")

		choix1 = input()

		print("\nChoisir un type de tri")
		print("1 - Ordre croissant")
		print("2 - Ordre décroissant")

		choix2 = input()

		if choix1 == '1' and choix2 == '1':
			var = weather.find().sort("City", 1)
			print(var)
			for a in var:
				pprint(a)
		elif choix1 == '1' and choix2 == '2':
			var = weather.find().sort("City", -1)
			for a in var:
				pprint(a)

		elif choix1 == '2' and choix2 == '1':
			var = weather.find().sort("Weather", 1)
			for a in var:
				pprint(a)
		elif choix1 == '2' and choix2 == '2':
			var = weather.find().sort("Weather", -1)
			for a in var:
				pprint(a)

		elif choix1 == '3' and choix2 == '1':
			var = weather.find().sort("Temp (°C)", 1)
			for a in var:
				pprint(a)
		elif choix1 == '3' and choix2 == '2':
			var = weather.find().sort("Temp (°C)", -1)
			for a in var:
				pprint(a)

		elif choix1 == '4' and choix2 == '1':
			var = weather.find().sort("Pressure (hPa)", 1)
			for a in var:
				pprint(a)
		elif choix1 == '4' and choix2 == '2':
			var = weather.find().sort("Pressure (hPa)", -1)
			for a in var:
				pprint(a)

		elif choix1 == '5' and choix2 == '1':
			var = weather.find().sort("Humidity (%)", 1)
			for a in var:
				pprint(a)
		elif choix1 == '5' and choix2 == '2':
			var = weather.find().sort("Humidity (%)", -1)
			for a in var:
				pprint(a)

		else: print("erreur")

	elif c == '6':
		ville = input("Ville a rechercher: ")
		var = weather.find({'City': ville})
		for a in var:
			pprint(a)

	else:
		print("Erreur")

def add_city():
	add_city = input("Veuillez entrer le nom de la ville\n")
	add_city = add_city.replace(" ", "+")
	print(add_city)
	add_country = input("Entrer le pays en format de type: fr, en, us...\n")
	file = open("Cities.txt", "a")
	file.write(add_city + "," + add_country + "\n")
	file.close()

        

def menu():
	os.system("cls")
	print("PROJET NOSQL ESILV 2020 - PEREZ Alexandre, GUESSOUS Alec\n\n")
	print("Selectionner une action: ")
	print("1 - Ajouter une ville dans la base de donnée")
	print("2 - Executer des requetes")
	print("3 - Quitter le programme")
	c = input()

	if c == "1":
		print("chargement de la database ...")
		data = register_data()
		insert_database(data)
		add_city()
	elif c == "2":
		print("chargement de la database ...")
		data = register_data()
		insert_database(data)
		requests_nosql()
	elif c == "3":
		return -1
	print("Appuyer sur entrer pour continuer")
	input()
	return 1


client = MongoClient('mongodb://localhost:27017')
db = client['database_weather']
weather = db.weather
stop = 1

while stop == 1:
	stop = menu()
