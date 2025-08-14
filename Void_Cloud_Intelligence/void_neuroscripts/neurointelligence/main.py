import neurokit2 as nk
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from huggingface_hub import login
import sys
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
from dotenv import load_dotenv

load_dotenv()

hf_token = os.getenv('HF_TOKEN')

login(token=hf_token)

model_name = "EleutherAI/pythia-160m"

# Initialize Chroma client
settings = Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chroma_db")
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="neuro_sessions")

# Load embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


#Load large model
try:
    print("Loading model with bfloat16 to save memory...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, device_map="cpu", torch_dtype=torch.bfloat16)
    print("Model loaded successfully.")
except Exception as e:
    print(f"An error occurred during model loading: {e}")
    # You can add more specific error handling here if needed.
    sys.exit(1)
    

    
    
def generate(prompt, profile):
    system_prompt = f"You're a {profile['tone']} assistant. Be {profile['style']}."
    full_prompt = system_prompt + "\nUser: " + prompt + "\nAI:"
    inputs = tokenizer(full_prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=500,
        do_sample=True,
        top_p=0.9,
        temperature=0.2, 
        repetition_penalty=1.2,
    )
    generated_tokens = outputs[0][inputs['input_ids'].size(1):]
    return tokenizer.decode(generated_tokens, skip_special_tokens=True)

def call_generate(eeg):
    print('calling generate')
    prompt = ('You are a neurophysiological data analyzer. Given a set of nueurological data, '
            'Decipher it and it and report its status. ' + eeg
    )
    profile = {'tone': "technical", 'style': "analytical"}
    response = generate(prompt, profile)
    return response
          

def simulate_eeg():
    return nk.eeg_simulate(duration=10, sampling_rate=256, noise=0.1)

def extract_embedding(signal):
    feature_text = " ".join(map(str, signal[:512]))
    return embedding_model.encode(feature_text)

def store_session(session_id, embedding, note):
    collection.add(
        ids=[session_id],
        embeddings=[embedding.tolist()],
        metadatas=[{"note": note}],
        documents=[note]
    )
    
def search_sessions(query, top_k=3):
    query_embedding = embedding_model.encode(query)
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )
    return results



def main():
    while True:
        cmd = input("Command (store/search/exit): ").strip().lower()

        if cmd == "store":
            print("Simulating EEG...")
            signal = simulate_eeg()
            
            #print('Signal reading: ' + str(signal))
            print(f'Signal reading: {signal}')
            print("Extracting embedding...")
            embedding = extract_embedding(signal)

            note = input("Enter a note for this session: ")
            session_id = input("Enter a session ID: ")
            print('Embedding reading: ' + str(embedding))
            
            analysis = call_generate(str(embedding[:80]))
            
            print(analysis)

            print("Storing session...")
            store_session(session_id, embedding, note)
            print("Session stored.\n")

        elif cmd == "search":
            query = input("Enter search query: ")
            print("Searching...\n")
            results = search_sessions(query)

            for i, doc in enumerate(results['documents'][0]):
                meta = results['metadatas'][0][i]
                print(f"{i+1}. Note: {doc}\n   Metadata: {meta}\n")

        elif cmd == "exit":
            break

        else:
            print("Unknown command.\n")


if __name__ == "__main__":
    main()