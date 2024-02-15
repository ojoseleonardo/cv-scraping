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
    
    # fazendo pesquisa
    position_url = f'https://www.linkedin.com/jobs/search/?currentJobId=3811633882&geoId=105871508&keywords={position}&location={city}&origin=JOB_SEARCH_PAGE_LOCATION_AUTOCOMPLETE&refresh=true'
    web.get(position_url)
    
    time.sleep(1)
    
    # filtrando mais recentes 
    
    # clicando em todos os filtros
    clicaXPATH('/html/body/div[5]/div[3]/div[4]/section/div/section/div/div/div/div/div/button')
    
    # clicando em mais recentes
    clicaXPATH('/html/body/div[3]/div/div/div[2]/ul/li[2]/fieldset/div/ul/li[1]/input')
    
    # clicando em submit
    clicaXPATH('/html/body/div[3]/div/div/div[3]/div/button[2]')
    
    x = 1
    while True:
        try:
            # scrollando para a vaga
            position_element = web.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[2]/div[1]/div/ul/li[{x}]/div/div/div/div[2]/div[1]/a/strong')
            scroll_origin = ScrollOrigin.from_element(position_element)
            ActionChains(web)\
                .scroll_from_origin(scroll_origin, 0, 200)\
                .perform()
            # clicando na vaga
            clicaXPATH_timeout(f'/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[2]/div[1]/div/ul/li[{x}]/div/div/div/div[2]/div[1]/a/strong', 5)
            
            # guardando titulo da vaga
            position_title = web.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[2]/div[1]/div/ul/li[{x}]/div/div/div/div[2]/div[1]/a/strong')
            print(position_title.text)
            
            # guardando texto do botão principal
            mainBtn_span_element = web.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]/div[4]/div/div/div/button/span')
                                                             
            if mainBtn_span_element.text != 'Candidatura simplificada':
                pass
            else:
                # clicando no btn candidatura simplificada
                clicaXPATH('/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]/div[4]/div/div/div/button')
                
                # verificando qual tipo de candidatura simples
                try:
                    btn_cv = web.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div/form/div/div[3]/div/div[2]/div[2]/button')
                    print('tipo 1')
                except NoSuchElementException:
                    print('tipo 2')
                    
                # fechando candidatura
                clicaXPATH('/html/body/div[3]/div/div/button')
                
                # clicando em descartar candidatura
                clicaXPATH('/html/body/div[3]/div[2]/div/div[3]/button[1]')
                
                # salvando vaga
                clicaXPATH("/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]/div[4]/div/button")
        except Exception as error:
            print(error)
            break        
        # iterador do loop
        x += 1

    time.sleep(10)
    
run()