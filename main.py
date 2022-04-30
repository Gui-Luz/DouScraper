from core.models.dou_scrapper import DouScrapper


if __name__ == '__main__':

    ds = DouScrapper('14-04-2022')
    ds.scrape()
