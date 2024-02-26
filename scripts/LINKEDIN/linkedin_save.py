import glob
import json
import keyword
import mimetypes
from os.path import dirname
import os
import sys
from threading import Thread
import time
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
import re
from datetime import date
import logging
from tqdm import tqdm
import customtkinter as ctk
from tkinter import *
import sv_ttk
from tkinter.font import Font

logging.basicConfig(level=logging.INFO, filename="fillForm.log", format="%(asctime)s - %(levelname)s - %(message)s ")


def timeout_clicaXPATH(value, timeout):
    clica = WebDriverWait(web, timeout).until(EC.presence_of_element_located((By.XPATH, value)))
    web.execute_script('arguments[0].click();', clica)
    time.sleep(2)
    
def double_clicaXPATH(value1, value2):
    try:
        clica = WebDriverWait(web, 5).until(EC.presence_of_element_located((By.XPATH, value1)))
        web.execute_script('arguments[0].click();', clica)
        time.sleep(2)
    except:
        clica = WebDriverWait(web, 120).until(EC.presence_of_element_located((By.XPATH, value2)))
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

def limpaXPATH(value):
    escreve = WebDriverWait(web, 120).until(EC.presence_of_element_located((By.XPATH, value)))
    escreve.clear()
    time.sleep(.5)

def scroll_to_element(element):
    scroll_origin = ScrollOrigin.from_element(element)
    ActionChains(web)\
            .scroll_from_origin(scroll_origin, 0, 200)\
            .perform()
    


options = webdriver.ChromeOptions()
chrome_options = webdriver.ChromeOptions()
CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
web = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
action = ActionChains(web)
link = 'https://br.linkedin.com/?src=go-pa&trk=sem-ga_campid.12619604099_asid.149519181115_crid.657343811716_kw.linkedin_d.c_tid.kwd-148086543_n.g_mt.e_geo.1001724&mcid=6821526239111716925&cid=&gad_source=1&gclid=EAIaIQobChMIvvWO7IuhhAMVQkVIAB0yngJDEAAYASAAEgKFqPD_BwE&gclsrc=aw.ds'
web.get(link)
web.maximize_window()
email = 'joseleonardosantoos@outlook.com'
password = '709404Leo'
position = 'Desenvolvedor full stack'
city = 'Brasília'
def run():
    # escrevendo email
    escreveXPATH('//*[@id="session_key"]', email)

    # escrevendo senha
    escreveXPATH('//*[@id="session_password"]', password)

    # clicando em submit
    clicaXPATH('//*[@id="main-content"]/section[1]/div/div/form/div[2]/button')

    # fazendo pesquisa
    position_url = f'https://www.linkedin.com/jobs/search/?currentJobId=3827238696&geoId=106057199&keywords=Desenvolvedor&location=Brasil&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&sortBy=DD'
    web.get(position_url)

    time.sleep(1)

    # limpando e escrevendo titulo da vaga
    position_input = '/html/body/div[5]/header/div/div/div/div[2]/div[1]/div/div/input[1]'
    limpaXPATH(position_input)
    escreveXPATH(position_input, position)

    # limpando e escrevendo localização
    city_input = '/html/body/div[5]/header/div/div/div/div[2]/div[2]/div/div/input[1]'
    limpaXPATH(city_input)
    escreveXPATH(city_input, city)

    # clicando em pesquisar
    clicaXPATH('/html/body/div[5]/header/div/div/div/div[2]/button[1]')

    # guardando url atual
    current_url = web.current_url
    

    x = 1
    y = 0
    while True:
        
        try:
            # scrollando para a vaga
            position_element = web.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[2]/div[1]/div/ul/li[{x}]/div/div/div/div[2]/div[1]/a/strong')
            
        except NoSuchElementException:
            x = 1
            y += 25
            
            # refatorando link da pagina
            current_url += f'&start={y}'
            # mudando pagina
            web.get(current_url)
            
            time.sleep(1)
            
            # scrollando para a vaga
            position_element = web.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[2]/div[1]/div/ul/li[{x}]/div/div/div/div[2]/div[1]/a/strong')
            
        try:
            
            # scrolando até o elemento
            scroll_to_element(position_element)
                
            # clicando na vaga
            timeout_clicaXPATH(f'/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[2]/div[1]/div/ul/li[{x}]/div/div/div/div[2]/div[1]/a/strong', 5)

            # guardando titulo da vaga
            position_title = web.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[2]/div[1]/div/ul/li[{x}]/div/div/div/div[2]/div[1]/a/strong')
            print(position_title.text)

            # guardando texto do botão principal
            mainBtn_span_element = web.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]/div[4]/div/div/div/button/span')

            # guardando XPATH do elemento botão salvar
            btn_salvarV1 = '/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]/div[4]/div/button'
            btn_salvarV2 = '/html/body/div[4]/div[3]/div[4]/div/div/main/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]/div[4]/div/button'
            
            
            if mainBtn_span_element.text != 'Candidatura simplificada':
                print('candidatura normal')
                
                # clicando no btn_salvar
                double_clicaXPATH(btn_salvarV1, btn_salvarV2)
            else:
                print('candidatura simplificada')
                
                 # clicando no btn_salvar
                double_clicaXPATH(btn_salvarV1, btn_salvarV2)
                
        except:
            print('end loop')
            break

        # iterador do loop
        x += 1

    time.sleep(10)

run()