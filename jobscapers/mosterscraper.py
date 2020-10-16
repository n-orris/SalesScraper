from math import ceil
import requests
from bs4 import BeautifulSoup


class MonsterScraper:
    pages_url = None
    posting_list = []

    def __init__(self, location, job_type):
        self.location = location
        self.job_type = job_type
        self.url = None

    def seturl(self):
        # Enter web page url and specifics
        url = 'https://www.monster.ca/jobs/search/?q=' + self.job_type + '&where=' + self.location
        result = requests.get(url)
        results_per_page = 25

        # Puts the page content into html format
        page = BeautifulSoup(result.content, 'html.parser')
        num_results = page.find('h2', class_='figure')
        # find number of pages to search
        num_jobs = num_results.text.strip().strip("(").strip(")").split()
        pages = ceil(int(num_jobs[0]) / results_per_page)
        self.url = url + "&stpage=1&page=" + str(pages)
        return self.url

    def setscaper(self, ):

        response = requests.get(self.url)
        page = BeautifulSoup(response.content, 'html.parser')
        results = page.find(id="ResultsContainer")
        # seperates individual job postings by class
        job_elem = results.find_all('section', class_="card-content")

        for job in job_elem:
            i = 0

            title_elem = job.find('h2', class_='title')
            company_elem = job.find('div', class_='company')
            location_elem = job.find('div', class_='location')
            date_elem = job.find('time')

            if None in (title_elem, company_elem, location_elem, date_elem):
                continue

            # print(title_elem.text.strip())
            print(company_elem.text.strip())
            # print(location_elem.text.strip())
            # (date_elem.text.strip())
            # print("--------------------------------")
