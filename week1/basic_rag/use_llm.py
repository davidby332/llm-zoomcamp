from week1.basic_rag.build_prompt import build_prompt
from week1.basic_rag.min_search import search
from week1.basic_rag.config import (
    question
)
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
openai_client = OpenAI()
search_results = search(question)

def calculate_usage(
        response, 
        input_price = 0.75 / 1_000_000, 
        output_price = 4.50 / 1_000_000
):
    
    return (
        response.usage.input_tokens * input_price +
        response.usage.output_tokens * output_price
    )

response = openai_client.responses.create(
    model = "gpt-5.4-mini",
    input = build_prompt(
        question = question,
        search_results = search_results
    )
)

if __name__ == "__main__":
    print(response.output[0].content[0].text)
    print(f"Total Cost {calculate_usage(response = response)}")