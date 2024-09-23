import chromadb
import os
import sys
DB_LOCATION =   "./db"
def main():
        client = chromadb.PersistentClient(path=DB_LOCATION)
        segments_collection = client.get_collection(
                name ="segments_cos"
                )
        videos_collection = client.get_collection(
                name ="videos"
                )
        
        args = sys.argv[1:]
        video_place = int(args[0])
        video_list = os.listdir('./videos')
        video_list.sort(reverse=False)
        try:
                #i = video_list.index(video_name)
                video_name = video_list[video_place]
                print(f'{video_name} is #{video_place} in list')
                seg = segments_collection.get(where={'video name':video_name})
                print(f'There are {len(seg["ids"])} segments in the db')
        except:
                print(f'{video_place} not found in list')

if __name__ == "__main__":
    main()