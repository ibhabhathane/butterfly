from bs4 import BeautifulSoup as bs
import requests

from time import sleep
import random

from .sql import db
from apscheduler.schedulers.background import BackgroundScheduler

from pyrogram.errors import FloodWait
from client import Config, NoteNews


def check_send():
    #website = "https://www.adorocinema.com/noticias-materias-especiais/"
    website = "https://estudenoifma.ifma.edu.br/"
    html = requests.get(website).content
    soup = bs(html, "html.parser")
    # author = "Adoro Cinema" #
    #title = str(soup.main.h2.a.string)
    #link = "https://www.adorocinema.com" + str(soup.main.h2.a.get("href"))
    link = str(soup.main.h3.a["href"])
    if link is not None:
        if db.get_link(website) == None:
            db.update_link(website, "*")
            return
        if link != db.get_link(website).link:
            message = f"Essa porra já saiu, olha aí: {link}"
            #message = f"""
#[\u200c]({link})🌐 | via **Adoro Cinema:** **[{title}]({link})**
#
#▫️ | Mantido por: @NoteZV
#"""
            try:
                #NoteNews.send_message(Config.LOG_CHANNEL, message)
                NoteNews.send_message("-1001165341477" , message)
                db.update_link(website, link)
            except FloodWait as e:
                print(f"FloodWait: {e.x} segundos")
                sleep(e.x)
            except Exception as e:
                print(str(e))
        else:
            print(f"FEED Verificado: {link}")
            
scheduler = BackgroundScheduler()
#scheduler.add_job(check_send, "interval", seconds=Config.CHECK_INTERVAL, max_instances=Config.MAX_INSTANCES)
scheduler.add_job(check_send, "interval", seconds=10, max_instances=200)
scheduler.start()
