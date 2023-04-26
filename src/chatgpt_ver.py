"""chatgpt version"""
import aiohttp
import asyncio


async def download_content(url='', temp_folder=''):
    """download"""
    async with aiohttp.ClientSession() as session:
        async with session.head(url) as response:
            filename = url.split("/")[-1]
            filepath = temp_folder + "/" + filename
            with open(filepath, "wb") as f:
                f.write(await response.read())



async def main():
    """main func"""
    readmd = 'https://gitea.radium.group/radium/project-configuration/src/branch/master/README.md'

    urls = [
        "https://gitea.radium.group/radium/project-configuration/src/branch/master/nitpick",
        "https://gitea.radium.group/radium/project-configuration/src/branch/master/LICENSE",
        readmd,
        "https://gitea.radium.group/radium/project-configuration.git",
    ]
    temp_folder = "./temp_folder"
    tasks = [asyncio.create_task(
        download_content(url, temp_folder)) for url in urls]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
