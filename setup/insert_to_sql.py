import time
from sqlitesearch import TextSearchIndex

from setup.import_data import import_docs

def create_db():

    documents = import_docs()
    doc_list = [
        doc 
        for doc 
        in documents 
        if doc["course"] == "llm-zoomcamp"
    ]

    index = TextSearchIndex(
        text_fields=["question", "section", "answer"],
        keyword_fields=["course"],
        db_path="./setup/faq.db"
    )

    for doc in doc_list:
        index.add(doc)
        print(f"""Added: {doc["question"][:60]}...""")
        time.sleep(0.5)

    index.close()

if __name__ =="__main__":
    create_db()