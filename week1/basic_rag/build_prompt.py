from week1.basic_rag.min_search import search
from week1.basic_rag.config import (
    USER_PROMPT_TEMPLATE,
    question
)

def build_context(search_results):
    lines = []

    for doc in search_results:
        lines.append(doc["section"])
        lines.append("Q: " + doc["question"])
        lines.append("A: " + doc["answer"])
        lines.append("")

    return "\n".join(lines).strip()

def build_prompt(question, search_results):
    context = build_context(search_results)
    prompt = USER_PROMPT_TEMPLATE.format(
        question=question,
        context=context
    )
    return prompt.strip()

search_results = search(question)

prompt = build_prompt(
    question = question, 
    search_results = search_results
)

if __name__ == "__main__":
    print(prompt)