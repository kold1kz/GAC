"""test case for radium"""
import os
from bs4 import BeautifulSoup
# import asyncio
# from loguru import logger
import requests
import wget


# logger.add("debug.log",
#            format="{time} {level} {message}",
#            level="DEBUG",
#            rotation="5MB")


def download_repo(url: str) -> bool:
    "download repo from git"
    domen_name = "https://" + url.split('/')[2]
    links = get_urls(url=url)
    if links:
        for link in links:
            download_link = get_download_urls(domen_name+link)
            print(download_link)
            if download_link:
                web_file_name = link.split('/')[-1]
                try:
                    wget.download(url=domen_name+download_link, out=web_file_name)
                except (IndexError, ValueError):
                    print("\nerror\n")
            else:
                os.mkdir(link.split('/')[-1])
                os.chdir(link.split('/')[-1])
                download_repo(domen_name+link)
    os.chdir("..")

    return True


def get_urls(url: str) -> list:
    """takes"""
    github = False
    post = []

    # if url.split('/')[2] == "github.com":
    #     github = True
    #     exceptions = ["github.com"]

    try:
        html = requests.get(url=url, timeout=5, stream=True,
                            allow_redirects=True).text

        doc = BeautifulSoup(html, "html.parser")
        for link in doc.find_all('a', href=True, class_=github, title=True,):
            # if github:
            #     if link['href'].split('/')[-1] not in exceptions:
            #         post.append(link['href'])
            # else:
            if link['href']:
                post.append(link['href'])
        return post

    except ValueError:
        print("ValueError")
        return None


def get_download_urls(url: str) -> str:
    """takes"""
    post = ""
    try:
        html = requests.get(url=url, timeout=5, stream=True,
                            allow_redirects=True).text
        doc = BeautifulSoup(html, "html.parser")
        for link in doc.find_all('a', href=True, download=True):
            if link['href']:
                post = link['href']
        return post

    except ValueError:
        print("ValueError")
        return None


if __name__ == "__main__":
    URL = 'https://gitea.radium.group/radium/project-configuration/src/branch/master'
    local_foldername = URL.split('/')[4]
    os.mkdir(local_foldername)
    os.chdir(local_foldername)
    download_repo(URL)
