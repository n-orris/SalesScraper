from jobscapers import monsterscraper
from jobscapers import Indeedscraper
import linkedin_jobs_scraper


def main():
    print("Web scraper initialized")

    if __name__ == "__main__":
        print("Start Main")


def startscrapers(search_terms, filter_fields, filter_kword, location, *args):
    monster = monsterscraper.MonsterScraper(search_terms, location)
    indeed = Indeedscraper.IndeedScraper(search_terms, location)
    # Eluta
    # Glassdoor
    # linkedin
    # Set Urls & # num of pages to scrap
    monster.seturl()
    indeed.seturl()

    # indeed.seturl()
    # scrape and collect lists
    # for x in search_terms:

    # add keywords and filter if applicable
    monster.setscaper()
    indeed.setscraper()

    if filter_kword is not None:
        if len(filter_kword) == 1:
            monster.filterbykeywords(a=filter_kword[0])
            indeed.filterbykeywords(a=filter_kword[0])
        elif len(filter_fields) == 2:
            monster.filterbykeywords(a=filter_kword[0], b=filter_kword[1])
            indeed.filterbykeywords(a=filter_kword[0], b=filter_kword[1])
        elif len(filter_fields) == 3:
            monster.filterbykeywords(a=filter_fields[0], b=filter_kword[1], c=filter_kword[2])
            indeed.filterbykeywords(a=filter_kword[0], b=filter_kword[1], c=filter_kword[2])
        else:
            monster.filterbykeywords(a=filter_kword[0], b=filter_kword[1], c=filter_kword[2], d=filter_kword[-1])
            indeed.filterbykeywords(a=filter_kword[0], b=filter_kword[1], c=filter_kword[2], d=filter_kword[-1])

    if filter_fields is not None:

        if len(filter_fields) == 1:
            monster.filterbyfield(a=filter_fields[0])
            indeed.filterbyfield(a=filter_fields[0])
        elif len(filter_fields) == 2:
            monster.filterbyfield(a=filter_fields[0], b=filter_fields[1])
            indeed.filterbyfield(a=filter_fields[0], b=filter_fields[1])

        elif len(filter_fields) == 3:
            monster.filterbyfield(a=filter_fields[0], b=filter_fields[1], c=filter_fields[2])
            indeed.filterbyfield(a=filter_fields[0], b=filter_fields[1], c=filter_fields[2])
        else:
            monster.filterbyfield(a=filter_fields[0], b=filter_fields[1], c=filter_fields[2], d=filter_fields[-1])
            indeed.filterbyfield(a=filter_fields[0], b=filter_fields[1], c=filter_fields[2], d=filter_fields[-1])


# startscrapers(['information security'], ['title', 'company'], ['security'], 'Canada')


monster = monsterscraper.MonsterScraper('Security', 'Canada')
indeed = Indeedscraper.IndeedScraper('Information Security', 'Canada')
# Eluta
# Glassdoor
# linkedin
# Set Urls & # num of pages to scrap
monster.seturl()
indeed.seturl()

# indeed.seturl()
# scrape and collect lists
# for x in search_terms:

# add keywords and filter if applicable
monster.setscaper()
indeed.setscraper()

monster.filterbyfield(a='title', b='company')
indeed.filterbyfield(a='title', b='company')
