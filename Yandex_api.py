#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
import wget
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass()
class YandexApi:
    images = []
    album = []

    def create_request(self, text='', size='', color='', type=''):
        """
        :param text: title of search e.g. boobs
        :param size: large or medium or small
        :param color: what color of image to search
        :param type: type of image available: jpg, png, gifan for gif
        :return: url request
        """

    def parse_images(self, text='', size='', color='', type='') -> list:
        """
        :param text: title of search e.g. boobs
        :param size: large or medium or small
        :param color: what color of image to search
        :param type: type of image available: jpg, png, gifan for gif
        :return: list of addresses
        """

        req = requests.get(f'https://yandex.ru/images/search?text={text}').text
        bs = BeautifulSoup(req, features="html.parser")
        items = bs.findAll("img", {"class": "serp-item__thumb justifier__thumb"})
        for img in items:
            self.images.append(str(img))
        for el in self.images:
            self.album.append(el.split(' ')[-1][7:-3])

        # print(self.album)
        return self.album

    def download_images(self):
        # скачиваем изображения в папку
        n = 0
        for el in self.parse_images(text='космос'):
            url = 'https://' + el
            wget.download(url, out=f'/root/PycharmProjects/Yandex_photos_downloader/album/{n}')
            n += 1


if __name__ == '__main__':
    yapi = YandexApi()
    yapi.download_images()
