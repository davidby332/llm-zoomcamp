# This implements minsearch and anindex
# minsearch is a package written by
# Alex Gregoriev

from setup.import_data import import_docs
from minsearch import Index

# Setup prompts

question = 'I just discovered the course. Can I join now?'

index = Index(
    text_fields=['question', 'section', 'answer'],
    keyword_fields=['course']
)

docs = import_docs()
index.fit(docs)

def search(question, course = 'llm-zoomcamp'):
    boost_dict = {'question': 2.0, 'section': 0.5}
    filter_dict = {"course": course}

    return index.search(
        question,
        boost_dict = boost_dict,
        filter_dict = filter_dict,
        num_results = 5
    )

if __name__ == "__main__":
    print('starting')
    print(search(question))
