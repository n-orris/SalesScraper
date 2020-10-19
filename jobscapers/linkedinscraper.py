import requests
import csv
from parsel import Selector
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(executable_path=r"C:\Users\taran\OneDrive\Desktop\chromedriver_win32\chromedriver.exe")
driver.get('https://www.linkedin.com/')

username = driver.find_element_by_name("session_key")
username.send_keys('scributleshax@gmail.com')
sleep(random.uniform(0.4, 0.7))

password = driver.find_element_by_name("session_password")
password.send_keys('123cabbage')
sleep(random.uniform(0.5, 0.8))

sign_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')
sign_in_button.click()
sleep(random.uniform(1.5, 3.5))


def scrapecompany():
    writer = csv.writer(open('output.csv', 'w+', encoding='utf-8-sig', newline=''))
    writer.writerow(['company', 'industry', 'employees', 'HQ', 'specialties', 'description'])

    driver.get("https://www.linkedin.com/company/optivainc/about/")
    sleep(random.uniform(2, 3.5))

    sel = Selector(text=driver.page_source)

    company = sel.xpath(
        '//*[@class = "org-top-card-summary__title t-24 t-black truncate"]/text()').extract


    industry = sel.xpath(
        '//*[@class = "org-page-details__definition-text t-14 t-black--light t-normal"]/text()').extract_first().split()
    industry = ' '.join(industry)

    employees = sel.xpath(
        '//*[@class = "org-page-details__employees-on-linkedin-count t-14 t-black--light mb5"]/text()').extract_first()

    hq = ' '.join(sel.xpath('//*[@class = "org-page-details__definition-text t-14 t-black--light '
                            't-normal"]/text()').extract_first().split())
    specialties = sel.xpath('//*[@class = "org-page-details__definition-text t-14 t-black--light t-normal"]/text()').extract_first()

    url = driver.current_url

    print('\n')
    print('Company: ', company)
    print('Industry: ', industry)
    print('Employees: ', employees)
    print('HQ: ', hq)
    print('Specialties:', specialties)
    # print('Description:', description)
    print('URL: ', url)
    print('\n')


def scrapeprofile():
    writer = csv.writer(open('output.csv', 'w+', encoding='utf-8-sig', newline=''))
    writer.writerow(['Name', 'Company', 'position', 'Location', 'URL'])

    driver.get('https://www.linkedin.com/in/robert-stabile-7a69b441/')
    sleep(2)

    sel = Selector(text=driver.page_source)

    name = sel.xpath('//*[@class = "inline t-24 t-black t-normal break-words"]/text()').extract_first().split()
    name = ' '.join(name)

    company = sel.xpath(
        '//*[@class = "pv-entity__secondary-title t-14 t-black t-normal"]/text()').extract_first().split()
    company = ' '.join(company) if company else None

    position = sel.xpath('//*[@class = "t-16 t-black t-bold"]/text()').extract_first().split()
    position = ' '.join(position)

    experience = sel.xpath('//*[@class = "pv-top-card-v3--experience-list"]')

    location = ' '.join(sel.xpath('//*[@class = "t-16 t-black t-normal inline-block"]/text()').extract_first().split())

    url = driver.current_url

    print('\n')
    print('Name: ', name)
    print('Company: ', company)
    print('Education: ', position)
    print('Location: ', location)
    print('URL: ', url)
    print('\n')

    writer.writerow([name,
                     company,
                     position,
                     location,
                     url])


scrapecompany()

driver.quit()
