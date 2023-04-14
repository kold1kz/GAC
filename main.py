"""test case for radium"""
import os
import urllib
import requests
from bs4 import BeautifulSoup
# import asyncio
from loguru import logger


logger.add("debug.log",
           format="{time} {level} {message}",
           level="DEBUG",
           rotation="5MB")


@logger.catch
def download_repo(url: str) -> bool:
    "download repo from git"
    logger.debug("download_repo START")
    domen_name = "https://" + url.split('/')[2]
    links = get_urls(url=url)

    if links:
        for link in links:
            download_urls = get_download_urls(domen_name+link)
            logger.info(f'get download urls = {download_urls}')
            if download_urls:
                download_file(domen_name+download_urls)
            else:
                logger.debug(f'no download link\nlink={domen_name+link}')
                os.mkdir(link.split('/')[-1])
                os.chdir(link.split('/')[-1])
                download_repo(domen_name+link)
    else:
        logger.warning('no links')
    os.chdir('..')

    return True


@logger.catch
def get_urls(url: str) -> list:
    """takes"""
    logger.debug("get_urls START")
    github = False
    post = []
    try:
        html = requests.get(url=url, timeout=5, stream=True,
                            allow_redirects=True).text

        doc = BeautifulSoup(html, "html.parser")
        for link in doc.find_all('a', href=True, class_=github, title=True,):
            logger.info(f'link from get_urls = {link}')
            if link['href']:
                post.append(link['href'])
        return post

    except urllib.error.HTTPError:
        logger.error('get_urls error')
        return None


@logger.catch
def get_download_urls(url: str, status=True) -> str:
    """takes"""
    logger.debug(f'get_download_urls START status = {status}')
    post = ""
    try:
        html = requests.get(url=url, timeout=5, stream=True,
                            allow_redirects=True).text
        doc = BeautifulSoup(html, "html.parser")
        links = doc.find_all('a', href=True, download=status)
        if links:
            for link in links:
                logger.info(f'link from doc ={link}')
                if link['href'] and check_download_link(link):
                    post = link['href']
        else:
            post = get_download_urls(url=url, status=False)
        return post

    except urllib.error.HTTPError:
        logger.error("get_download_urls error")
        return None

    # except ValueError:
    #     logger.error(f'not download link(except): {link}')
    #     return None

    # except EOFError:
    #     logger.error(f'not download link(except): {link}')
    #     return None
        


@logger.catch
def download_file(url: str,) -> bool:
    """file download"""
    logger.debug("download_file START")
    try:
        web_file_name = url.split('/')[-1]
        response = requests.get(url=url, stream=True, timeout=10)
        with open(web_file_name, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024*1024):
                if chunk:
                    file.write(chunk)
    except urllib.error.HTTPError:
        logger.error('download_file error')
        return False
    return True


@logger.catch
def check_download_link(url: str) -> bool:
    """check for raw"""
    logger.debug('check_download_link START')
    elems = url.split('/')
    for elem in elems:
        if elem == 'raw':
            return True
    return False


if __name__ == "__main__":
    # URL = 'https://gitea.radium.group/radium/project-configuration/src/branch/master'
    URL = 'https://gitea.radium.group/radium/flatfilecms'
    local_foldername = URL.split('/')[4]
    os.mkdir(local_foldername)
    os.chdir(local_foldername)
    download_repo(URL)
