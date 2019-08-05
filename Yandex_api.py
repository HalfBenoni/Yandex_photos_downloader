#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import wget
from dataclasses import dataclass
from fake_useragent import UserAgent
from TorCrawler import TorCrawler
import time


@dataclass()
class YandexApi:
    images = []
    album = []

    def create_params(self, text, page_num=None, size=None, color=None, file=None) -> dict:
        """
        :param page_num: number of pages to be parsed
        :param text: title of search e.g. boobs (is required)
        :param size: large, medium or small
        :param color: what color of image to search e.g. black
        :param file: type of image available: jpg for jpeg, png & gifan for gif
        :return: a url request
        """
        params = {}

        params['text'] = text

        if page_num is not None:
            params['p'] = page_num

        if size is not None:
            params['isize'] = size

        if color is not None:
            params['icolor'] = color

        if file is not None:
            params['itype'] = file

        # req = requests.get(url, params=params)
        # print(req.url)

        return params

    def get_image_links(self, num_of_pages) -> list:
        """
        :param num_of_pages: number of pages you want to parse
        (1 page is a visible part of screen equals to 30 img or smth like that)
        :return a list of links to the images
        """

        crawler = TorCrawler(ctrl_pass='16:3DE78CE013BBC3AC60E6045CE1310E5C95BF78DBC300B592796399FE46')

        url = 'https://yandex.ru/images/search'
        header = {'User-Agent': UserAgent().chrome}
        cur_page = 0  # current page (0 at the bening)

        while cur_page != num_of_pages:

            param = self.create_params(text='космос', page_num=cur_page, color='black')
            req = crawler.get(url, headers=header, params=param)

            items = req.findAll("img", {"class": "serp-item__thumb justifier__thumb"})

            for img in items:
                self.images.append(img.attrs['src'])

            for img in items:
                # формируем список из ссылок на изображения, находящихся в атрибуте src
                self.images.append(img.attrs['src'][2:])

            cur_page += 1
            time.sleep(5)

        # for el in self.images:
        #     print(el)
        # print(len(self.images))

        return self.images

    def get_orinal_images(self, num_of_pages) -> list:

        orig_album = []

        crawler = TorCrawler(ctrl_pass='16:3DE78CE013BBC3AC60E6045CE1310E5C95BF78DBC300B592796399FE46')

        url = 'https://yandex.ru/images/search'
        header = {'User-Agent': UserAgent().chrome}
        cur_page = 0  # current page (0 at the bening)

        while cur_page != num_of_pages:

            param = self.create_params(text='космос', page_num=cur_page, color='black')
            req = crawler.get(url, headers=header, params=param)

            items = req.findAll("a", {"class": "serp-item__link"})

            for img in items:
                orig_album.append(img.attrs['href'])

            cur_page += 1
            time.sleep(5)

        return orig_album

    def download_images(self):
        # скачиваем изображения в папку

        n = 1  # имена изображений
        for el in self.get_image_links(num_of_pages=3):
            # формируем корректную ссылку для скачивания
            link = 'https://' + el
            wget.download(link, out=f'/root/PycharmProjects/Yandex_photos_downloader/album/{n}')
            n += 1


if __name__ == '__main__':
    yapi = YandexApi()
    yapi.download_images()
    # yapi.get_image_links(num_of_pages=3)