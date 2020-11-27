from math import ceil
import requests
from bs4 import BeautifulSoup
import csv


# writes contents of a list to choosen file


class IndeedScraper:
    pages_url = None
    posting_list = []
    data = None
    outputlist = []
    fieldvalues = None
    kwords = []

    def __init__(self, job_type, location):
        self.location = location
        self.kwords = job_type
        self.url = None
        self.runs = []

    def seturl(self):
        # Enter web page url and specifics
        i = 0
        for kword in self.kwords:
            self.url = "https://ca.indeed.com/jobs?q=" + kword + "&l=" + self.location + "&start=200000"
            response = requests.get(self.url)
            page = BeautifulSoup(response.content, 'html.parser')
            page_num = page.find('div', class_='pagination')
            last_pages = page_num.text.strip()
            self.runs.append(int(last_pages[-2:]))
            print(self.runs)
            i += 1

    def setscraper(self):
        for nums in range(0, len(self.kwords)):
            url_num = 0

            num = 0
            # runs scraper for each page of results
            for s in range(0, self.runs[url_num]):
                num += 10
                url = self.url + "&start=" + str(num)

                response = requests.get(url)
                page = BeautifulSoup(response.content, 'html.parser')
                # seperates individual job postings by class
                results = page.find_all('div', attrs={'data-tn-component': 'organicJob'})

                for job in results:
                    location = job.find('span', class_="location accessible-contrast-color-location")
                    title = job.find('a', attrs={'data-tn-element': "jobTitle"})
                    company_name = job.find('a', attrs={'data-tn-element': "companyName"})
                    summary = job.find('div', class_="summary")
                    date = job.find('span', class_='date')

                    if None in (job, company_name):
                        continue

                    posting = {
                        "title": title.text.strip(),
                        "company": company_name.text.strip(),
                        "location": location.text.strip(),
                        "date": date.text.strip(),
                        "summary": summary.text.strip()
                    }
                    self.posting_list.append(posting)
                num += 1
            url_num += 1

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
            elif any(ele.lower() in post["summary"].lower() for ele in filters.values()):
                filteredlist.append(post)

        self.outputlist = filteredlist
        print(self.outputlist)

    # outputs indeed job search data to csv file
    def tofile(self, file):
        with open(file, "w+", newline='') as csvfile:

            if self.fieldvalues is None:
                writer = csv.DictWriter(csvfile, fieldnames=["title", "company", "location", "date", "summary"])
                writer.writeheader()

                for data in self.outputlist:
                    writer.writerow(data)
            else:
                writer = csv.writer(csvfile)
                writer

                for data in self.outputlist:
                    writer.writerow(data)
