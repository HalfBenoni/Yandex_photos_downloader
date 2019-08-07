#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import wget
import socks
import socket
import requests
import subprocess
from bs4 import BeautifulSoup
from urllib.parse import unquote
from dataclasses import dataclass
from fake_useragent import UserAgent


@dataclass()
class YandexApi:
    images = []  # a list for preview images's links
    links = []  # a list for origin. images's links
    url = 'https://yandex.ru/images/search'
    header = {'User-Agent': UserAgent().chrome}
    cur_page = 0  # current page (0 at the bening)

    def changeIP(self) -> 'new IP':
        """
        to allow IP changing run:
        ~# service tor start (on Unix)
        ~# tor (on osX)
        """
        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
        socket.socket = socks.socksocket

        # reboot tor for IP changing
        os.system('service tor restart')
        time.sleep(5)

        # get the IP value
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

    def get_preview_images(self, num_of_pages: int) -> 'small images':
        """
        :param num_of_pages: number of pages you want to parse
        (1 page is a visible part of screen equals to 30 img or smth like that)
        :return a list of links to the images
        """
        while self.cur_page != num_of_pages:
            # each iteration will change the page_num parameter
            param = self.create_params(text='космос', page_num=self.cur_page, color='black')

            req = requests.get(self.url, headers=self.header, params=param).text
            bs = BeautifulSoup(req, features="html.parser")
            items = bs.findAll("img", {"class": "serp-item__thumb justifier__thumb"})

            # create a list of links to images that are in the src attribute
            for img in items:
                self.images.append(img.attrs['src'][2:])

            self.cur_page += 1
            time.sleep(5)

        self.download_preview_images()

    def get_orinal_images(self, num_of_pages: int) -> 'HQ images':

        orig_album = []

        while self.cur_page != num_of_pages:

            param = self.create_params(text='космос', page_num=self.cur_page, color='black')
            req = requests.get(self.url, headers=self.header, params=param).text
            bs = BeautifulSoup(req, features="html.parser")
            items = bs.findAll("a", {"class": "serp-item__link"})

            # create a list of formatted links to primary sources of images
            for img in items:
                orig_album.append(img.attrs['href'][1:])

            self.cur_page += 1
            time.sleep(5)

        for el in orig_album:
            s = unquote(el)
            self.links.append(s.split('&')[3][8:])

        self.download_origin_images()

    def download_preview_images(self):
        # download images to the folder
        direc = self.folder('preview_album')
        n = 0  # image name (required for python wget module)

        for el in self.images:
            # form the correct download link
            link = 'https://' + el
            try:
                # if the wget system command fails,
                # the execution is passed to the python wget module
                subprocess.check_output(f'wget -t 2 -nc -P {direc} {link}', shell=True)

            except subprocess.CalledProcessError as e:
                print(e)

                try:
                    requests.get(link, timeout=5)  # check if the site responds to the request
                    wget.download(link, out=f'{direc}/{n}')
                    n += 1

                except OSError as e:
                    # if the site denies access, skip it
                    print(e)
                    print('следующее изображение\n')
                    continue

                except requests.exceptions.Timeout as err:
                    # if the site does not respond, skip it
                    print("Timeout Error:", err)
                    print('Сайт не отвечает\n')
                    continue

    def download_origin_images(self):
        # download images to the folder
        direc = self.folder('origin_album')
        n = 0  # image name (required for python wget module)

        for url in self.links:
            try:
                # if the wget system command fails,
                # the execution is passed to the python wget module
                subprocess.check_output(f'wget -t 2 -nc -P {direc} {url}', shell=True)

            except subprocess.CalledProcessError as e:
                print(e)
                try:
                    requests.get(url, timeout=5)  # check if the site responds to the request
                    wget.download(url, out=f'{direc}/{n}')
                    n += 1

                except OSError as e:
                    # if the site denies access, skip it
                    print(e)
                    print('\nследующее изображение')
                    continue

                except requests.exceptions.Timeout as err:
                    # if the site does not respond, skip it
                    print("\nTimeout Error:", err)
                    print('\nСайт не отвечает')
                    continue

    def folder(self, name: str) -> object:
        # create a folgers for images
        if os.path.exists(path=os.getcwd() + '/' + name) is True:
            print(f"\nFile exists: {os.getcwd()}/{name}")

        else:
            print(f'Creating a folder: {os.getcwd()}/{name}')
            os.mkdir(path=os.getcwd() + '/' + name)
            print('Created')

        return os.path.abspath(f"{os.getcwd()}/{name}")


if __name__ == '__main__':
    yapi = YandexApi()
    yapi.changeIP()
    # yapi.get_preview_images(num_of_pages=1)
    # yapi.get_orinal_images(num_of_pages=1)
