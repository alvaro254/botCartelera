# coding=utf-8
from application import bot
import re
import bs4
from json import *
import requests

latitude = float('nan')
longitude = float('nan')

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@bot.message_handler(commands=['cartelera'])
def cartelera(message):

	titulos, infos, horarios = parsear("")

	for x in range(0, len(titulos)):

		bot.send_message(message.chat.id, titulos[x] + '\n' + infos[x] + '\n' + horarios[x]+ '\n')

def parsear(url):

	r = requests.get("https://www.mabuse.es/cartelera/Cordoba")

	soup = bs4.BeautifulSoup(r.text, 'html.parser')
	info_peliculas = soup.find_all("div", class_="informacion-pelicula")

	titulos_lista = list()
	infos_lista = list()
	horas_lista = list()

	for info_pelicula in info_peliculas:

		#Titulo pelicula
		titulos = info_pelicula.find_all(href=re.compile(".*pelicula/.*"))
		
		for titulo in titulos:

			#if titulo.text != " " and titulo.text not in titulos_lista:
			titulos_lista.append(titulo.text)
			#print titulo.text

		#Info pelicula
		infos = info_pelicula.find_all(string=re.compile(".*min\.$"))
		
		for info in infos:

			#if info.string not in infos_lista:
			infos_lista.append(info.string)
			#print info.string

		#Horario
		horas = info_pelicula.find_all(string=re.compile("[0-9]+:[0-9]+"))
		
		for hora in horas:

			horas_lista.append(hora.string)
			#print (hora.string)

	return titulos_lista, infos_lista, horas_lista

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    """
    Hace un 'eco' de lo que se recibe y no se ha procesado en algún comando anterior.
    :param message:
    :return:
    """
    bot.reply_to(message, message.text)
