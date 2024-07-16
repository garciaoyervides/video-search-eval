import sys
import time
from upload import process_video_to_db
import os
import logging
logger = logging.getLogger(__name__)

def main():
    videos_processed = 0
    videos_not_processed = 0
    args = sys.argv[1:]
    print(time.strftime('%l:%M%p %Z on %b %d, %Y'))
    logger.info(time.strftime('%l:%M%p %Z on %b %d, %Y'))
    if len(args) == 2:
        #process all videos in batches
        start_video = (int(args[0]))
        end_video = (int(args[1]))
        video_list = os.listdir('./videos')
        video_list.sort(reverse=False)
        print(f"{len(video_list)} videos  to be processed")
        logger.info(f"{len(video_list)} videos  to be processed")
        msg = ""
        for i,file in enumerate(video_list):
            if i >= start_video and i < end_video:
                if file.endswith(".mp4"):
                    try:
                        msb = f"./msb/{file.replace('.mp4', '.msb')}"
                        if os.path.isfile(msb):
                            response = process_video_to_db(file)
                            if response:
                                videos_processed += 1
                                msg = (f"{file} was processed successfully")
                            else:
                                videos_not_processed += 1
                                msg = (f"{file} was not processed")
                        else:
                            videos_not_processed += 1
                            msg = (f"{file} segmentation file not available")
                    except:
                        videos_not_processed += 1
                        msg = (f"{file} segmentation file not available")
                    print(msg)
                    logger.info(msg)
    print(f"{videos_processed} videos processed")
    logger.info(f"{videos_processed} videos processed")
    print(f"{videos_not_processed} videos NOT processed")
    logger.info(f"{videos_not_processed} videos NOT processed")

    print(time.strftime('%l:%M%p %Z on %b %d, %Y'))
    logger.info(time.strftime('%l:%M%p %Z on %b %d, %Y'))

if __name__ == "__main__":
    main()