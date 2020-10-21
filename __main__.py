from jobscapers import monsterscraper
from jobscapers import Indeedscraper




search_term = "cyber"
location = "Canada"
monstertest = monsterscraper.MonsterScraper(search_term, location)
indeedtest = Indeedscraper.IndeedScraper(search_term, location)


def main():
    print("Web scraper initialized")

    if __name__ == "__main__":
        print("Start Main")


monstertest.seturl()
monstertest.setscaper()
monstertest.filterbyfield(a="title", b="company")




