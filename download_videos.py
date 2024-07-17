import urllib.request
from bs4 import BeautifulSoup
from urllib.request import urlopen
import socket
import sys
import os
import logging
logger = logging.getLogger(__name__)
socket.setdefaulttimeout(15)

def get_video_link(url):
  html_page = urlopen(url)
  soup = BeautifulSoup(html_page, features="lxml")
  for link in soup.findAll('a'):
    if ".mp4" in str(link.get('href')):
      return(str(link.get('href')))


def main(args):
    if len(args)== 2:
        start_video = (int(args[0]))
        end_video = (int(args[1]))

        logging.basicConfig(filename='myapp.log', level=logging.INFO)
        with open('list of videos.xml', 'r') as f:
            data = f.read()
        from bs4 import BeautifulSoup
        Bs_data = BeautifulSoup(data,"xml")

        filenames = Bs_data.find_all('filename')
        sources = Bs_data.find_all('source')
        filenames = list(map(lambda txt: str(txt).replace('<filename>', '').replace('</filename>', ''), filenames))
        sources = list(map(lambda txt: str(txt).replace('<source>', '').replace('</source>', ''), sources))
        files = zip(filenames,sources)
        sorted_files = sorted(files, key=lambda x: x[0])

        if not os.path.exists("./videos"):
            os.makedirs("./videos")
        downloaded_videos = 0
        not_downloaded_videos=0
        for i,file in enumerate(sorted_files):
            if i >= start_video and i <end_video:
                file_name = file[0]
                file_url = file[1]
                try:
                    print(f'{i} {file_url}/{get_video_link(file_url)}')
                    logger.info(f'{i} {file_url}/{get_video_link(file_url)}')
                    urllib.request.urlretrieve(f'{file_url}/{get_video_link(file_url)}', f'./videos/{file_name}')
                    downloaded_videos += 1
                except:
                    print(f"{i} {file_name} not available")
                    logger.info(f"{i} {file_name} not available")
                    not_downloaded_videos += 1

        print(f'VIDEO DOWNLOAD ENDED : {start_video}-{end_video}, {downloaded_videos} downloaded, {not_downloaded_videos} not downloaded')
        logger.info(f'VIDEO DOWNLOAD ENDED : {start_video}-{end_video}, {downloaded_videos} downloaded, {not_downloaded_videos} not downloaded')
                
if __name__ == "__main__":
    main(sys.argv[1:])