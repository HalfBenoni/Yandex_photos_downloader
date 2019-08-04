#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import requests
import wget
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass()
class YandexApi:
    images = []
    album = []

    def create_params(self, text, page_num=None, size=None, color=None, file=None) -> str:
        """
        :param page_num: number of pages to be parsed
        :param text: title of search e.g. boobs (is required)
        :param size: large, medium or small
        :param color: what color of image to search e.g. black
        :param file: type of image available: jpg for jpeg, png & gifan for gif
        :return: a url request
        """
        params = {'text': text}

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

    def parse_images(self, num_of_pages) -> list:
        """
        :param num_of_pages: number of pages you want to parse
        (1 page is a visible part of screen or smth like that)
        :return a list of links to the images
        """
        url = 'https://yandex.ru/images/search'
        cur_page = 0  # current page (0 at the bening)

        while cur_page != num_of_pages:

            req = requests.get(url, params=self.create_params(text='космос', page_num=cur_page, color='white')).text

            bs = BeautifulSoup(req, features="html.parser")
            items = bs.findAll("img", {"class": "serp-item__thumb justifier__thumb"})

            # for img in items:
            #     print(img)

            for img in items:
                self.images.append(str(img))
            for el in self.images:
                print(el)
            # for el in self.images:
            #     self.album.append(el.split(' ')[-1][7:-3])
            cur_page += 1

        # print(self.album)
        # print(len(self.album))
        # return self.album

    # def download_images(self):
    #     # скачиваем изображения в папку
    #     n = 1
    #     for el in self.parse_images(text='космос'):
    #         url = 'https://' + el
    #         wget.download(url, out=f'/root/PycharmProjects/Yandex_photos_downloader/album/{n}')
    #         n += 1


if __name__ == '__main__':
    yapi = YandexApi()
    yapi.parse_images(num_of_pages=3)