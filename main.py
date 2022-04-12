from core.models.dou_scrapper import DouScrapper


if __name__ == '__main__':

    #ds = DouScrapper('01-01-2022', '25-03-2022')
    ds = DouScrapper('11-04-2022')
    ds.scrape()
