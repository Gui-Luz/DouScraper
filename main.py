import os
from core.models.dou_scrapper import DouScrapper


if __name__ == '__main__':

    ROOT_PATH = os.getcwd()

    ds = DouScrapper('15-01-2021')
    ds.scrape()
