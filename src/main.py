import os
import pandas as pd
from dotenv import load_dotenv
import openai
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from chromadb.config import Settings

from get_tokens import num_tokens

# initial settings
load_dotenv()
API_KEYS = os.environ['API_KEYS']
EMBEDDING_MODEL = 'text-embedding-ada-002'
BATCH_SIZE = 1000

openai.api_key = API_KEYS

def create_embeddings_text(texts):
    embeddings = []
    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i:i+BATCH_SIZE]
        response = openai.Embedding.create(
            model=EMBEDDING_MODEL,
            input=batch
        )
        embeddings.extend(response['data'])
    return embeddings

def create_embeddings(items):
    embeddings = []
    for batch_start in range(0, len(items), BATCH_SIZE):
        batch_end = batch_start + BATCH_SIZE
        batch = items[batch_start:batch_end]
        print(f'Batch {batch_start} to {batch_end-1}')
        response = openai.Embedding.create(
            model=EMBEDDING_MODEL,
            input=batch
        )
        for i, be in enumerate(response['data']):
            assert i == be['index'] # double check embeddings are in same order as input
        batch_embeddings = [e['embedding'] for e in response['data']]
        embeddings.extend(batch_embeddings)

    df = pd.DataFrame({'text': items, 'embedding': embeddings})
    return df

def create_chroma_client():
    persist_directory = 'chroma_persistence'
    chroma_client = chromadb.Client(
        Settings(
            persist_directory=persist_directory,
            chroma_db_impl="duckdb+parquet",
        )
    )
    return chroma_client

def chroma_collection(chroma_client):
    chroma_client.reset()
    collection_name = 'stevie_collection'
    embedding_function = OpenAIEmbeddingFunction(api_key=API_KEYS, model_name=EMBEDDING_MODEL)
    collection = chroma_client.create_collection(name=collection_name, embedding_function=embedding_function)
    return collection

def query_collection(
        query: str,
        collection: chromadb.api.models.Collection.Collection,
        max_results: int=100) -> tuple[list[str], list[float]]:
    results = collection.query(query_texts=query, n_results=max_results, include=['documents', 'distances'])
    strings = results['documents'][0]
    relatednesses = [1 - x for x in results['distances'][0]]
    return strings, relatednesses

if __name__=='__main__':
    # data.jsonlをDataFrameで読み込み
    path_data = os.path.join('data', 'data.jsonl')
    df_data = pd.read_json(path_data, orient='records', lines=True)

    # QuestionとAnswerを結合
    df_data['QnA'] = df_data['Question'] + ' ' + df_data['Answer']
    # token取得
    df_data['token_QnA'] = df_data['QnA'].apply(num_tokens)

    # tokenが4000以上のものは除外
    df_data = df_data[df_data['token_QnA'] < 4097].reset_index(drop=True)

    # for debug
    df_data = df_data.head()

    # IT NEED COST
    items = df_data['QnA'].to_list()
    df_embedding = create_embeddings(items=items)

    # settings for chromacb
    chroma_client = create_chroma_client()
    stevei_collection = chroma_collection(chroma_client)
    stevei_collection.add(
        ids = df_embedding.index.astype(str).tolist(),
        documents=df_embedding['text'].tolist(),
        embeddings=df_embedding['embedding'].tolist(),
    )
    chroma_client.persist()

    # response
    strings, relatednesses = query_collection(
        collection=stevei_collection,
        query='会計検査員の検査について教えて下さい',
        max_results=3,
    )

    for string, relatednesses in zip(strings, relatednesses):
        print(f'{relatednesses=:.3f}')
        print(string)
