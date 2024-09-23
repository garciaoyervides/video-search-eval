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
        video_name = args[0]
        video_list = os.listdir('./videos')
        video_list.sort(reverse=False)
        try:
                i = video_list.index(video_name)
                print(f'{video_name} is #{i} in list')
        except:
                print(f'{video_name} not found in list')
        seg = segments_collection.get(where={'video name':video_name})
        print(f'There are {len(seg["ids"])} segments in the db')

if __name__ == "__main__":
    main()