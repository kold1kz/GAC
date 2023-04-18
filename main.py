"""test case for radium"""
import os
import urllib
import asyncio
import requests
from bs4 import BeautifulSoup
from loguru import logger


logger.add("debug.log",
           format="{time} {level} {message}",
           level="DEBUG",
           rotation="5MB")


@logger.catch
def download_repo(url: str) -> bool:
    "download repo from git"
    logger.debug("download_repo START")
    try:
        domen_name = "https://" + url.split('/')[2]
        links = get_urls(url=url)

        url_href_num = create_href_check(url)
        links = check_list(links, url_href_num)

        if links:
            for link in links:
                logger.debug(f'\n\n\tlink in work: {link}\n')
                download_urls = get_download_urls(domen_name+link)
                logger.debug(f'get download urls = {download_urls}')
                if download_urls:
                    download_file(domen_name+download_urls)
                else:
                    logger.debug(f'no download link\nlink={domen_name+link}')
                    os.mkdir(link.split('/')[-1])
                    os.chdir(link.split('/')[-1])
                    download_repo(domen_name+link)
        else:
            logger.warning('check link')
            folder_name = url.split('/')[-1]
            os.rmdir('../'+folder_name)
        os.chdir('..')

    except IndexError:
        logger.error(f'check link: {url}')
        return None

    except requests.exceptions.ConnectionError:
        logger.error('Name or service not known')
        return None

    return True


@logger.catch
def check_list(links: list[str], num: int) -> list[str]:
    """deleate link to back folder"""
    ver = 0
    while ver < len(links):
        if len(links[ver]) <= num:
            links.pop(ver)
        else:
            ver += 1
    return links


@logger.catch
def get_download_urls(url: str, status=True) -> str:
    """takes"""
    logger.debug(f'get_download_urls START status = {status}')
    post = ""
    try:
        html = requests.get(url=url, timeout=5, stream=True,
                            allow_redirects=True).text
        doc = BeautifulSoup(html, "html.parser")
        links = doc.find_all('a', href=True, download=status,
                             class_=False, click=False, target=False)
        if links:
            for link in links:
                logger.debug(f'link from doc ={link["href"]}')
                if link['href'] and check_download_link(link['href']):
                    post = link['href']
                    return post
            return None
        else:
            post = get_download_urls(url=url, status=False)
        return post

    except urllib.error.HTTPError:
        logger.error("get_download_urls error")
        return None

    except ValueError:
        logger.error(f'error link: {link}')
        return None

    except EOFError:
        logger.error(f'no download link(except): {link}')
        return None


@logger.catch
def create_href_check(url: str) -> int:
    """create href from str"""
    perem = url.split('/')[3:-1]
    out = ''
    for elem in perem:
        out += '/'
        out += elem
    return len(out)


@logger.catch
def check_download_link(url: str) -> bool:
    """check for raw"""
    logger.debug('check_download_link START')
    elems = url.split('/')[3:-1]
    for elem in elems:
        if elem == 'raw':
            return True
    return False


@logger.catch
def get_urls(url: str) -> list:
    """takes"""
    logger.debug("get_urls START")
    github = False
    post = []
    try:
        html = requests.get(
            url=url,
            timeout=5,
            stream=True,
            allow_redirects=True
        ).text

        doc = BeautifulSoup(html, "html.parser")
        for link in doc.find_all(
                'a',
                href=True,
                class_=github,
                title=True,
                click=False,
                arget=False
        ):
            logger.info(f'link from get_urls = {link["href"]}')
            if link['href']:
                post.append(link['href'])
        return post

    except urllib.error.HTTPError:
        logger.error('get_urls error')
        return None

    except ValueError:
        logger.error(f'error link, please check link: {url}')
        return None

    except EOFError:
        logger.error(f'not download link(except): {url}')
        return None

    except requests.exceptions.ConnectionError:
        logger.error(f'Name or service not known: {url}')
        return None


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


if __name__ == "__main__":
    logger.debug('\n\n\n\tstart program\n\n\n')
    URL = input("input URL: ")
    try:
        local_foldername = URL.split('/')[-1]
        os.mkdir(local_foldername)
        os.chdir(local_foldername)
        download_repo(URL)
    except FileExistsError:
        logger.error('file already created')
