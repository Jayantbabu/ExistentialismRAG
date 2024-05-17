import sqlite3
import pandas as pd
from datasets import Dataset
from transformers import DPRContextEncoder, DPRContextEncoderTokenizer, RagTokenizer, RagRetriever, RagTokenForGeneration, StoppingCriteriaList, MaxLengthCriteria
import logging
from transformers import BartTokenizer
from transformers.generation.stopping_criteria import EosTokenCriteria

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data_from_db(db_path):
    conn = sqlite3.connect(db_path)
    query = "SELECT title, content FROM books"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

books_df = load_data_from_db('./books.db')

books_dataset = Dataset.from_pandas(books_df)
books_dataset = books_dataset.rename_column("content", "text")
tokenizer = DPRContextEncoderTokenizer.from_pretrained('facebook/dpr-ctx_encoder-single-nq-base')
model = DPRContextEncoder.from_pretrained('facebook/dpr-ctx_encoder-single-nq-base')

def embed_books(examples):
    inputs = tokenizer(examples['text'], return_tensors='pt', padding=True, truncation=True, max_length=512)
    outputs = model(**inputs)
    return {'embeddings': outputs.pooler_output.detach().numpy()}

books_dataset = books_dataset.map(embed_books, batched=True)
books_dataset.add_faiss_index(column='embeddings')

rag_tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-nq")
eos_token_id = tokenizer.eos_token_id
model.config.eos_token_id = eos_token_id
retriever = RagRetriever.from_pretrained("facebook/rag-token-nq", index_name="custom", indexed_dataset=books_dataset)
rag_model = RagTokenForGeneration.from_pretrained("facebook/rag-token-nq", retriever=retriever)

def generate_response(query):
    input_ids = rag_tokenizer(query, return_tensors="pt").input_ids
    logging.info("Tokenization complete. Generating response...")
    output_ids = rag_model.generate(input_ids, temperature=0.9, top_k=50, max_length=50)
    return rag_tokenizer.decode(output_ids[0], skip_special_tokens=True)

query = "What is Existentialism?"
response = generate_response(query)
print(response)