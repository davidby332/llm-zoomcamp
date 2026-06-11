from minsearch import Index
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv
from sqlitesearch import TextSearchIndex

from setup.import_data import import_docs

from week1.basic_rag.config import (
    INSTRUCTIONS,
    USER_PROMPT_TEMPLATE,
    question
)

load_dotenv()

class RAGBase:

    def __init__(
        self,
        index,
        llm_client,
        instructions = INSTRUCTIONS,
        prompt_template = USER_PROMPT_TEMPLATE,
        course = "llm-zoomcamp",
        model = "gpt-5.4-mini"
    ):
        self.index = index
        self.llm_client = llm_client
        self.instructions = instructions
        self.course = course
        self.prompt_template = prompt_template
        self.model = model

    def search(
            self,
            question, 
        ):

        boost_dict = {'question': 2.0, 'section': 0.5}
        filter_dict = {"course": self.course}

        return self.index.search(
            question,
            boost_dict = boost_dict,
            filter_dict = filter_dict,
            num_results = 5
        )
    
    def build_context(
            self,
            search_results
        ):

        lines = []

        for doc in search_results:
            lines.append(doc["section"])
            lines.append("Q: " + doc["question"])
            lines.append("A: " + doc["answer"])
            lines.append("")

        return "\n".join(lines).strip()

    def build_prompt(
            self,
            question, 
        ):

        context = self.build_context(
            self.search(question)
        )

        prompt = USER_PROMPT_TEMPLATE.format(
            question=question,
            context=context
        )

        return prompt.strip()
    
    def llm(self, prompt):
        
        input_messages = [
            {"role": "developer", "content": self.instructions},
            {"role": "user", "content": prompt}
        ]

        response = self.llm_client.responses.create(
            model=self.model,
            input=input_messages
        )

        return response.output_text
    
    def rag(self, question):
        prompt = self.build_prompt(question = question)
        answer = self.llm(prompt)
        return answer

if __name__ == "__main__":

    if Path('./setup/faq.db').exists():
        index = TextSearchIndex(
            text_fields=["question", "section", "answer"],
            keyword_fields=["course"],
            db_path="./setup/faq.db"
        )
    
    else:
        print('No index found')

        index = Index(
            text_fields=['question', 'section', 'answer'],
            keyword_fields=['course']
        )

        docs = import_docs()
        index.fit(docs)

    rag_base = RAGBase(
        index = index,
        llm_client = OpenAI(),
        instructions = INSTRUCTIONS,
        prompt_template = USER_PROMPT_TEMPLATE,
        course = "llm-zoomcamp",
        model = "gpt-5.4-mini"
    )

    print(rag_base.rag(question = question))