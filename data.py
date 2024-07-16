import clip
import torch
import chromadb

global device
global model
global preprocess
global videos_collection
global segments_collection
global logs_collection

DB_LOCATION =   "./db"

#SETUP
try:
  # Load the model
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load('ViT-B/32', device)
    print("Device loaded: " + str(device))
except:
    print("Error loading model and data")
    exit()
try:
    client = chromadb.PersistentClient(path=DB_LOCATION)
    #client = chromadb.HttpClient(host='localhost', port=8000)
    videos_collection = client.get_or_create_collection(
        name ="videos",
        metadata={"hnsw:space": "cosine"}
        )
    segments_collection = client.get_or_create_collection(
        name ="segments_cos",
        metadata={"hnsw:space": "cosine"}
        )
    logs_collection = client.get_or_create_collection(
        name ="logs",
        metadata={"hnsw:space": "cosine"}
        )
    print("Database loaded") 
except:
    print("Database Error")
    exit()