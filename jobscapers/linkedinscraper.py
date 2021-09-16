from parsel import Selector
from bs4 import BeautifulSoup
from selenium import webdriver
import random
import csv
from time import sleep
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, ExperienceLevelFilters
from linkedin_scraper import Company

companylist = []

# driver = webdriver.Chrome()
# driver.get('https://www.linkedin.com/')
#
# username = driver.find_element_by_name("session_key")
# username.send_keys('')
# sleep(random.uniform(10, 20))
#
# password = driver.find_element_by_name("session_password")
# password.send_keys()
# sleep(random.uniform(1, 2.7))
#
# sign_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')
# sign_in_button.click()
# sleep(random.uniform(4, 6))


def job_scraper(query, locations):
    jobs = []

    writer = csv.writer(open('../data/output/linkedin/linkedin_jobs.csv', 'w+', encoding='utf-8-sig', newline=''))
    writer.writerow(
        ['Title', 'Company', 'Date', 'URL', 'Description', 'Job Function', 'Industries', 'Location', 'site'])

    def on_data(data: EventData):
        jobs.append([data.title, data.company, data.date, data.link, data.description, data.job_function
                        , data.industries, data.location, 'Linkedin'])

    def on_error(error):
        print('[ON_ERROR]', error)

    def on_end():
        print('[ON_END]')
        print(jobs)

        for job in jobs:
            writer.writerow(job)

    scraper = LinkedinScraper(
        chrome_options=None,  # You can pass your custom Chrome options here
        headless=True,  # Overrides headless mode only if chrome_options is None
        max_workers=6,
        # How many threads will be spawned to run queries concurrently (one Chrome driver for each thread)
        slow_mo=0.4,  # Slow down the scraper to avoid 'Too many requests (429)' errors
    )

    # Add event listeners
    scraper.on(Events.DATA, on_data)
    scraper.on(Events.ERROR, on_error)
    scraper.on(Events.END, on_end)

    queries = [
        Query(
            options=QueryOptions(
                optimize=True,  # Blocks requests for resources like images and stylesheet
                limit=1  # Limit the number of jobs to scrape
            )
        ),
        Query(
            query=query,
            options=QueryOptions(
                locations=locations,
                optimize=False,
                limit=5,
                filters=QueryFilters(
                    company_jobs_url=None,
                    # Filter by companies
                    relevance=RelevanceFilters.RELEVANT,
                    time=TimeFilters.MONTH,
                    type=None,
                    experience=None,
                )
            )
        ),
    ]
    scraper.run(queries)


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
    writer = csv.writer(open('../data/output/linkedin/linkedin_companies.csv', 'w+', encoding='utf-8-sig', newline=''))
    writer.writerow(['company', 'industry', 'status', 'channel', 'where', 'progress', 'domain', 'based', 'employees',
                     'job posting', 'HQ', 'description', 'specialties', 'Linkedin'])

    entries = []
    reader = open('../data/input/linkedin_entrylist.txt', 'r')
    for line in reader.readlines():
        entries.append(line)
        print(line)

    for url in entries:
        driver.get(url)
        sleep(random.uniform(1.5, 2.5))
        site = driver.page_source

        soup = BeautifulSoup(site, 'html.parser')
        page = soup.findAll(attrs={"class": "org-page-details__definition-text t-14 t-black--light t-normal"})

        if page is None:
            continue

        company = soup.find('h1', class_='org-top-card-summary__title t-24 t-black truncate')
        employees = soup.find('span', class_='v-align-middle')
        employees = employees.text.strip() if employees else None
        overview = soup.find('p', class_='break-words white-space-pre-wrap mb5 t-14 t-black--light t-normal')
        address = soup.find('div', class_='org-locations-module__map-container--small relative')

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
    writer = csv.writer(open('../data/output/linkedin/linkedin_profiles.csv', 'w+', encoding='utf-8-sig', newline=''))
    writer.writerow(['Name', 'Company', 'position', 'Location', 'URL'])

    entries = []
    reader = open('../data/input/linkedprofileurls.csv', 'r')
    for line in reader.readlines():
        entries.append(line)

    for url in entries:
        driver.get(url)
        sleep(random.uniform(1, 2))

        sel = Selector(text=driver.page_source)

        name = sel.xpath('//*[@class = "inline t-24 t-black t-normal break-words"]/text()').extract_first().split()
        name = ' '.join(name)

        company = sel.xpath(
            '//*[@class = "pv-entity__secondary-title t-14 t-black t-normal"]/text()').extract_first().split()
        company = ' '.join(company) if company else None

        position = sel.xpath('//*[@class = "t-16 t-black t-bold"]/text()').extract_first().split()
        position = ' '.join(position)

        experience = sel.xpath('//*[@class = "pv-top-card-v3--experience-list"]')

        location = ' '.join(
            sel.xpath('//*[@class = "t-16 t-black t-normal inline-block"]/text()').extract_first().split())

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


def pulljobs():
    term = 'security'
    driver.get('https://www.linkedin.com/company/medallia-inc./jobs/')
    search_term = driver.find_element_by_xpath(
        '/html/body/div[7]/div[3]/div/div[3]/div[2]/div[2]/section/div/div/div/div/div[1]/div/input')
    search_term.send_keys(term)
    sleep(random.uniform(0.5, 1.7))
    search_button = driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div[3]/div[2]/div[2]/section/div/div/a')
    search_button.click()
    sleep(random.uniform(5, 10))
    titles = driver.find_elements_by_xpath('//*[@id="ember621"]')
    locations = driver.find_elements_by_xpath(
        '/html/body/div[8]/div[3]/div[3]/div/div/div/div/section/div/ul/li[2]/div/div/div[1]/div[2]/div[3]/ul/li')
    jobs = driver.find_elements_by_class_name(
        'job-card-container relative job-card-list job-card-container--clickable '
        'job-card-list--underline-title-on-hover jobs-search-results-list__list-item--active '
        'jobs-search-two-pane__job-card-container--viewport-tracking-1')
    sleep(2)
    print(driver.current_url)


testlst = ['https://www.linkedin.com/company/big-viking-games/about',
           'https://www.linkedin.com/company/sledgehammer-games/about/',
           'https://www.linkedin.com/company/turbulent/about/']


def valid_links():
    writer = csv.writer(open('../data/output/linkedin/linkedin_urls.csv', 'w+', encoding='utf-8-sig', newline=''))

    entries = []
    reader = open('../data/input/linkedin_entrylist.txt', 'r')
    for line in reader.readlines():
        entries.append(line)

    for url in entries:
        driver.get(url)
        sleep(random.uniform(1, 2))
        site = driver.page_source

        soup = BeautifulSoup(site, 'html.parser')
        page = soup.findAll(attrs={"class": "org-page-details__definition-text t-14 t-black--light t-normal"})

        company = soup.find('h1', class_='org-top-card-summary__title t-24 t-black truncate')
        employees = soup.find('span', class_='v-align-middle')

        if None in (company, employees):
            writer.writerow("Null")
            print(None)
        else:
            writer.writerow([url])
            print(url)


job_scraper('sec', 'canada')
