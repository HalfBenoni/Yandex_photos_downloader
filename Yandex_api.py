#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import wget
import socks
import socket
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
from dataclasses import dataclass
from fake_useragent import UserAgent


@dataclass()
class YandexApi:
    """
    to start changing IP run:
    ~# service tor start (on Unix)
    ~# tor (on osX)
    """

    def changeIP(self):

        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
        socket.socket = socks.socksocket

        # перезапускаем tor для смены IP
        os.system('service tor restart')
        time.sleep(5)

        ip = requests.get('http://checkip.dyndns.org').content
        soup = BeautifulSoup(ip, 'html.parser')
        newIP = soup.find('body').text

        print(newIP)

    def create_params(self, text, page_num=None, size=None, color=None, file=None) -> dict:
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

        return params

    def get_preview_images(self, num_of_pages) -> list:
        """
        :param num_of_pages: number of pages you want to parse
        (1 page is a visible part of screen equals to 30 img or smth like that)
        :return a list of links to the images
        """

        url = 'https://yandex.ru/images/search'
        header = {'User-Agent': UserAgent().chrome}
        cur_page = 0  # current page (0 at the bening)
        images = []

        while cur_page != num_of_pages:
            # при каждой итерации будет меняться параметр page_num
            param = self.create_params(text='космос', page_num=cur_page, color='black')

            req = requests.get(url, headers=header, params=param).text
            bs = BeautifulSoup(req, features="html.parser")

            items = bs.findAll("img", {"class": "serp-item__thumb justifier__thumb"})

            for img in items:
                # формируем список из ссылок на изображения, находящихся в атрибуте src
                images.append(img.attrs['src'][2:])

            cur_page += 1
            time.sleep(5)

        # for el in self.images:
        #     print(el)
        # print(len(self.images))

        return images

    def get_orinal_images(self, num_of_pages) -> list:

        orig_album = []
        links = []

        url = 'https://yandex.ru/images/search'
        header = {'User-Agent': UserAgent().chrome}
        cur_page = 0  # current page (0 at the bening)

        while cur_page != num_of_pages:

            param = self.create_params(text='космос', page_num=cur_page, color='black')
            req = requests.get(url, headers=header, params=param).text
            bs = BeautifulSoup(req, features="html.parser")

            items = bs.findAll("a", {"class": "serp-item__link"})

            # формируем список из форматированных сллыок на первоисточники изображений
            for img in items:
                orig_album.append(img.attrs['href'][1:])

            cur_page += 1
            time.sleep(5)

        for el in orig_album:
            s = unquote(el)
            links.append(s.split('&')[3][8:])

        return links

    def download_preview_images(self):

        n = 0  # имена изображений
        for el in self.get_preview_images(num_of_pages=3):
            # формируем корректную ссылку для скачивания
            link = 'https://' + el
            wget.download(link, out=f'/root/PycharmProjects/Yandex_photos_downloader/preview_album/{n}')
            n += 1

    def download_origin_images(self):
        # скачиваем изображения в папку

        n = 0  # имена изображений
        for el in self.get_orinal_images(num_of_pages=1):
            try:
                requests.get(el, timeout=5)  # проверяеем, отвечает ли сайт на запрос
                wget.download(el, out=f'/root/PycharmProjects/Yandex_photos_downloader/origin_album/{n}')
                n += 1

            except OSError as e:
                # если сайт отказывает в доступе, пропускаем его
                print(e)
                print('следующее изображение')
                # changeIP()
                continue

            except requests.exceptions.Timeout as errt:
                # если сайт не отвечает, пропускаем его
                print("Timeout Error:", errt)
                continue


if __name__ == '__main__':
    yapi = YandexApi()
    yapi.changeIP()
    yapi.download_origin_images()
    # yapi.get_orinal_images(num_of_pages=1)
