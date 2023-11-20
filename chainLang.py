from langchain.chains import create_extraction_chain
from langchain.chat_models import ChatOpenAI
import os

os.environ['OPENAI_API_KEY'] = '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'

# Schema
schema = {
    "properties": {
        "product_name": {"type": "string"},
        "quantity": {"type": "integer"},
        "price_per_unit": {"type": "string"},
    },
    "required": [],
}

# Input
inp = """30 llaves inglesas que vale 300 pesos cada una"""
# Run chain
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k", max_tokens=8000)
chain = create_extraction_chain(schema, llm)
response = chain.run(inp)

print(response)