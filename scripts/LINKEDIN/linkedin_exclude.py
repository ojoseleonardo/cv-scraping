import glob
import json
import keyword
import mimetypes
from os.path import dirname
import os
import sys
from threading import Thread
import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from openpyxl import load_workbook
import re
from datetime import date
import logging
from tqdm import tqdm
import customtkinter as ctk
from tkinter import *
import sv_ttk
from tkinter.font import Font

logging.basicConfig(level=logging.INFO, filename="fillForm.log", format="%(asctime)s - %(levelname)s - %(message)s ")

def ultimoArquivo(diretorioEtipo):
    listaArquivos = glob.glob(diretorioEtipo)
    arquivo = max(listaArquivos, key=os.path.getctime)
    return arquivo

def move_to_download_folder(downloadPath, newFileName, fileExtension):
    got_file = False   
    ## Grab current file name.
    while got_file == False:
        try: 
            ultimoArquivo(dirDownload+f"/*{fileExtension}")
            logging.info('movendo arquivo para pasta pdfs...')
            got_file = True

        except:
            logging.warning("Aguarde! O dowload está sendo processado...")
            time.sleep(20)

    ## Create new file name
    fileDestination = downloadPath+"\\"+newFileName+fileExtension
    time.sleep(5)

    os.rename(ultimoArquivo(dirDownload+f"/*{fileExtension}"), fileDestination)

    return

def clicaXPATH_timeout(value, timeout):
    clica = WebDriverWait(web, timeout).until(EC.presence_of_element_located((By.XPATH, value)))
    web.execute_script('arguments[0].click();', clica)
    time.sleep(2)
    
def clicaXPATH(value):
    clica = WebDriverWait(web, 120).until(EC.presence_of_element_located((By.XPATH, value)))
    web.execute_script('arguments[0].click();', clica)
    time.sleep(2)
    
def escreveXPATH(value, text):
    escreve = WebDriverWait(web, 120).until(EC.presence_of_element_located((By.XPATH, value)))
    escreve.send_keys(text)
    time.sleep(.5)
    
def apagaFileDowload():
    filelist = glob.glob(os.path.join(dirDownload, "*.pdf"))
    for f in filelist:
            logging.info("to aq apagando")
            os.remove(f) 
            
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

dirExecutavel = os.path.join(application_path)

dirDownload = dirExecutavel+"\\downloads"
dirPdfs = dirExecutavel+"\\pdfs"

options = webdriver.ChromeOptions()
chrome_options = webdriver.ChromeOptions()
settings = {
"recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": "",
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2,
}
prefs = {
         'download.prompt_for_download': False,
         'plugins.always_open_pdf_externally': True,
         'download.default_directory' : dirDownload,
         'printing.print_preview_sticky_settings.appState': json.dumps(settings), 
          "savefile.default_directory": dirDownload,
         }
options.add_experimental_option('prefs', prefs)
options.add_argument('--kiosk-printing')
CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
web = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(web, 12)
action = ActionChains(web)
link = 'https://br.linkedin.com/?src=go-pa&trk=sem-ga_campid.12619604099_asid.149519181115_crid.657343811716_kw.linkedin_d.c_tid.kwd-148086543_n.g_mt.e_geo.1001724&mcid=6821526239111716925&cid=&gad_source=1&gclid=EAIaIQobChMIvvWO7IuhhAMVQkVIAB0yngJDEAAYASAAEgKFqPD_BwE&gclsrc=aw.ds'
web.get(link)
web.maximize_window()
email = 'joseleonardosantoos@outlook.com'
password = '709404Leo'
position = 'Desenvolvedor%20Java'
city = 'S%C3%A3o%20Paulo%2C%20Brasil'
def run():
    # escrevendo email
    escreveXPATH('//*[@id="session_key"]', email)
    
    # escrevendo senha
    escreveXPATH('//*[@id="session_password"]', password)
    
    # clicando em submit
    clicaXPATH('//*[@id="main-content"]/section[1]/div/div/form/div[2]/button')
    
    # clicando e vagas
    clicaXPATH('//*[@id="global-nav"]/div/nav/ul/li[3]/a')
    
    # clicando em minhas vagas
    clicaXPATH('/html/body/div[5]/div[3]/div/div[3]/div/div/div/div[1]/nav/div/ul/li[1]/a')
    
    # clicando em salvas
    clicaXPATH('/html/body/div[5]/div[3]/div/main/section/div/div[1]/ul/li[1]/button')
    
    x = 1
    while True:
        try:
            # clicando na vaga
            clicaXPATH_timeout(f'/html/body/div[5]/div[3]/div/main/section/div/div[2]/div/ul/li[1]/div/div/div/div[2]/div[1]/div[1]/div/span/span/a', 5)
                
            # excluindo dos salvos
            clicaXPATH('/html/body/div[5]/div[3]/div[2]/div/div/main/div/div[1]/div/div[1]/div/div/div[1]/div[4]/div/button')
            
            # voltando para vagas salvas
            web.back()
            # contador 
            x += 1
        except:
            break
            
run()