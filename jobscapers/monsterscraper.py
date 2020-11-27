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
    kwords = None
    url_list = []

    def __init__(self, job_type, location):
        self.location = location
        self.kwords = job_type
        self.url = None
        self.pages = None
        self.runs = []

    def seturl(self):
        # Enter web page url and specifics

        self.url = 'https://www.monster.ca/jobs/search/?q=' + self.kwords + '&where=' + self.location

        result = requests.get(self.url)
        results_per_page = 25

        # Puts the page content into html format
        page = BeautifulSoup(result.content, 'html.parser')
        header = page.find_all('h2', class_='figure')
        num = header[0].text.strip().strip("(").strip(")").split()[0]
        print(num)
        # find number of pages to search
        num_jobs = num
        self.pages = ceil(int(num) / results_per_page)
        self.runs.append(ceil(self.pages / 10))
        self.url_list.append(self.url)

    # scrapes job posting data and inserts into  a list of dictionaries
    def setscaper(self):
        for num in range(0, len(self.kwords)):
            url_num = 0

            for s in range(0, self.runs[url_num]):
                x = 0
                num = 10
                if x == 0:
                    url = self.url_list[url_num] + "&stpage=1&page=10"
                else:
                    url = self.url[url_num] + "&stpage=" + str(
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
            url_num += 0

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
        print(self.outputlist)

        # filters by chosen dictionary fields

    def filterbyfield(self, **filters):
        filteredlist = []
        self.fieldvalues = filters.values()

        if len(self.outputlist) <= 1:
            for post in self.posting_list:
                if len(filters) == 0:
                    filteredlist.append(post)
                else:
                    entry = []
                    for f in filters.values():
                        entry.append(post[f])
                        filteredlist.append(entry)

                    self.outputlist = filteredlist
            print(self.outputlist)

        else:
            for post in self.outputlist:
                if len(filters) == 0:
                    filteredlist.append(post)
                else:
                    entry = []
                    for f in filters.values():
                        entry.append(post[f])
                    filteredlist.append(entry)
            self.outputlist = filteredlist
            print(self.outputlist)

    def tofile(self, file):
        with open(file, "w+", newline='') as csvfile:

            if self.fieldvalues is None or self.outputlist is None:
                writer = csv.DictWriter(csvfile, fieldnames=["title", "company", "location", "date"])
                writer.writeheader()

                for data in self.posting_list:
                    writer.writerow(data)
            else:
                writer = csv.writer(csvfile)
                writer

                for data in self.outputlist:
                    writer.writerow(data)

    def getpostings(self):
        return self.posting_list
