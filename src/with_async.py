"""test case for radium"""
import os
import urllib
import asyncio
import aiofiles
import aiohttp
import requests
from bs4 import BeautifulSoup
from loguru import logger


logger.add("debug.log",
           format="{time} {level} {message}",
           level="DEBUG",
           rotation="5MB")


@logger.catch
async def download_repo(url: str) -> bool:
    "download repo from git"
    logger.debug("download_repo START")
    try:
        domen_name = "https://" + url.split('/')[2]
        folder_name = url.split('/')[-1]
        links = await get_urls(url=url)

        url_href_num = create_href_check(url)
        links = check_list(links, url_href_num)

        if links:
            for link in links:
                logger.debug(f'\n\n\tlink in work: {link}\n')
                download_urls = await get_download_urls(domen_name+link)
                logger.debug(f'get download urls = {download_urls}')
                if download_urls:
                    await download_file(domen_name+download_urls)
                else:
                    logger.debug(f'no download link\nlink={domen_name+link}')
                    os.mkdir(link.split('/')[-1])
                    os.chdir(link.split('/')[-1])
                    await download_repo(domen_name+link)
        else:
            logger.warning(f'check link:\nlinks: {links}')
            os.rmdir('../'+folder_name)
        os.chdir('..')

    except IndexError:
        logger.error(f'check link: {url}')
        os.rmdir('../'+folder_name)
        return False

    except requests.exceptions.ConnectionError:
        logger.error('Name or service not known')
        os.rmdir('../'+folder_name)
        return False
    except TypeError:
        logger.error('Type error')
        os.rmdir('../'+folder_name)
        return False

    return True


@logger.catch
async def get_urls(url: str) -> list:
    """takes"""
    logger.debug("get_urls START")
    github = True
    post = []
    try:
        async with aiohttp.ClientSession() as session:
            html = await session.get(
                url=url,
                timeout=5,
                # stream=True,
                # allow_redirects=True
            )

            doc = BeautifulSoup(await html.text(), "html.parser")
            docs = doc.find_all(
                'a',
                href=True,
                class_=github,
                title=True,
                click=False,
                target=False
            )

            for link in docs:
                logger.info(f'link from get_urls = {link["href"]}')
                if link['href']:
                    print(link['href'])
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
async def get_download_urls(url: str, status=True) -> str:
    """takes"""
    logger.debug(f'get_download_urls START status = {status}')
    post = ""
    try:
        async with aiohttp.ClientSession() as session:
            html = await session.get(
                url=url, timeout=5
            )
            doc = BeautifulSoup(await html.text(), "html.parser")
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
                post = await get_download_urls(url=url, status=False)
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
async def download_file(url: str,) -> bool:
    """file download"""
    logger.debug("download_file START")
    try:
        async with aiohttp.ClientSession() as session:
            web_file_name = url.split('/')[-1]
            response = await session.get(url=url, timeout=10)
            data = await response.read()
            async with aiofiles.open(web_file_name, "wb") as file:
                await file.write(data)
    except urllib.error.HTTPError:
        logger.error('download_file error')
        return False
    except TypeError:
        logger.error('Type Error')
        return False
    return True


@logger.catch
def main() -> bool:
    """main func"""
    logger.debug('\n\n\n\tstart program\n\n\n')
    input_url = input("input URL: ")
    # input_url = 'https://gitea.radium.group/radium/project-configuration'
    try:
        local_foldername = input_url.split('/')[-1]
        os.mkdir(local_foldername)
        os.chdir(local_foldername)
        asyncio.run(download_repo(input_url))
    except FileExistsError:
        logger.error('folder already created')
        return False
    return True


if __name__ == "__main__":
    os.exit(main())
