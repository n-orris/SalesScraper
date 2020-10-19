from math import ceil
import requests
from bs4 import BeautifulSoup
import csv


# writes contents of a list to choosen file


class MonsterScraper:
    pages_url = None
    posting_list = []
    data = None
    outputlist = []
    fieldvalues = None

    def __init__(self, job_type, location):
        self.location = location
        self.job_type = job_type
        self.url = 'https://www.monster.ca/jobs/search/?q=' + self.job_type + '&where=' + self.location
        self.pages = None
        self.runs = None

    def seturl(self):
        # Enter web page url and specifics
        result = requests.get(self.url)
        results_per_page = 25

        # Puts the page content into html format
        page = BeautifulSoup(result.content, 'html.parser')
        num_results = page.find('h2', class_='figure')
        # find number of pages to search
        num_jobs = num_results.text.strip().strip("(").strip(")").split()
        self.pages = ceil(int(num_jobs[0]) / results_per_page)
        self.runs = ceil(self.pages / 10)
        return self.pages

    # scrapes job posting data and inserts into  a list of dictionaries
    def setscaper(self):
        for s in range(0, self.runs):
            x = 0
            num = 10
            if x == 0:
                url = self.url + "&stpage=1&page=10"
            else:
                url = self.url + "&stpage=" + str(
                    num) + '&page=' + str(num + 10)

            response = requests.get(url)
            page = BeautifulSoup(response.content, 'html.parser')
            results = page.find(id="ResultsContainer")
            # seperates individual job postings by class
            job_elem = results.find_all('section', class_="card-content")

            for job in job_elem:
                i = 0

                title_elem = job.find('h2', class_='title')
                company_elem = job.find('span', class_='name')
                location_elem = job.find('div', class_='location')
                date_elem = job.find('time')

                # remove invalid entries
                if None in (title_elem, company_elem, location_elem, date_elem):
                    continue

                posting = {
                    'title': title_elem.text.strip(),
                    'company': company_elem.text.strip(),
                    'location': location_elem.text.strip(),
                    'date': date_elem.text.strip()
                }

                self.posting_list.append(posting)
                i += 1

        # filters by chosen dictionary fields

    def filterbyfield(self, **filters):
        filteredlist = []
        self.fieldvalues = filters.values()
        for post in self.posting_list:
            if len(filters) == 0:
                filteredlist.append(post)
            else:
                entry = []
                for f in filters.values():
                    entry.append(post[f])
                filteredlist.append(entry)

        self.outputlist = filteredlist
        print(filteredlist)
        return filteredlist

    # filters by specific keywords in the posting
    def filterbykeywords(self, **filters):
        filteredlist = []
        # reset header values
        self.fieldvalues = None
        for post in self.posting_list:

            if any(ele.lower() in post["title"].lower() for ele in filters.values()):
                filteredlist.append(post)
            elif any(ele.lower() in post["company"].lower() for ele in filters.values()):
                filteredlist.append(post)
            elif any(ele.lower() in post["location"].lower() for ele in filters.values()):
                filteredlist.append(post)

            elif any(ele.lower() in post["date"].lower() for ele in filters.values()):
                filteredlist.append(post)

        self.outputlist = filteredlist
        return filteredlist

    def tofile(self, file):
        with open(file, "w+", newline='') as csvfile:

            if self.fieldvalues is None:
                writer = csv.DictWriter(csvfile, fieldnames=["title", "company", "location", "date"])
                writer.writeheader()

                for data in self.outputlist:
                    writer.writerow(data)
            else:
                writer = csv.writer(csvfile)
                writer

                for data in self.outputlist:
                    writer.writerow(data)
