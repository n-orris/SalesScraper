import requests
import csv
from parsel import Selector
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
import random

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
sleep(random.uniform(50, 80))

companylist = []


def companysearch():

    num = 1
    for x in range(0, 3):
        num += 1
        url = 'https://www.linkedin.com/search/results/companies/?keywords=computer%20games&origin=GLOBAL_SEARCH_HEADER' \
              '&page=' + str(num)
        driver.get(url)

        sleep(random.uniform(1.5, 2))
        site = driver.page_source
        soup = BeautifulSoup(site, 'html.parser')
        page = soup.find('ul', class_='reusable-search__entity-results-list list-style-none')
        for a in page.find_all('a', href=True):
            if a['href'] in companylist:
                continue
            elif 'job' in str(a['href']):
                continue
            companylist.append(str(a['href']))




def scrapecompany():
    writer = csv.writer(open('../data/output/linkedincompany.csv', 'w+', encoding='utf-8-sig', newline=''))
    writer.writerow(['company', 'industry','status','channel','where','progress','domain', 'based', 'employees',
                     'job posting', 'HQ', 'description', 'specialties', 'Linkedin'])

    for url in companylist:
        driver.get(url+'about/')
        sleep(random.uniform(1.5, 2.5))
        site = driver.page_source

        soup = BeautifulSoup(site, 'html.parser')
        page = soup.findAll(attrs={"class": "org-page-details__definition-text t-14 t-black--light t-normal"})

        company = soup.find('h1', class_='org-top-card-summary__title t-24 t-black truncate')
        employees = soup.find('span', class_='v-align-middle')
        employees = employees.text.strip() if employees else None
        overview = soup.find('p', class_='break-words white-space-pre-wrap mb5 t-14 t-black--light t-normal')
        linkedin_url = url
        if len(page) < 6:
            continue
        website = page[0]
        industry = page[1]
        hq = page[2]
        specialties = page[5]

        if None in (company, employees, overview, website, industry, hq, specialties):
            continue

        stats = {
            'company': company.text.strip(),
            'employees': employees[8:21],
            'industry': industry.text.strip(),
            'hq': hq.text.strip(),
            'url': website.text.strip(),
            'overview': overview.text.strip(),
            'specialties': specialties.text.strip()
        }

        writer.writerow([company.text.strip(),
                         industry.text.strip(),
                         None,
                         None,
                         None,
                         None,
                         website.text.strip(),
                         None,
                         employees[8:21],
                         None,
                         overview.text.strip(),
                         hq.text.strip(),
                         specialties.text.strip(),
                         linkedin_url])



def scrapeprofile():
    writer = csv.writer(open('../data/output/linkedinprofiles.csv', 'w+', encoding='utf-8-sig', newline=''))
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


testlst = ['https://www.linkedin.com/company/big-viking-games/about',
           'https://www.linkedin.com/company/sledgehammer-games/about/',
           'https://www.linkedin.com/company/turbulent/about/']

scrapeprofile()

driver.quit()
