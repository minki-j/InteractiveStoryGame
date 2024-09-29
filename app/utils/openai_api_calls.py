from typing import List, Dict
from pydantic import BaseModel
from openai import OpenAI


def openai_api_structured_output_call(model: str, messages: List[Dict[str, str]], response_format: BaseModel):
    client = OpenAI()
    completion = client.beta.chat.completions.parse(
        model=model,
        messages=messages,
        response_format=response_format,
    )

    message = completion.choices[0].message
    if message.parsed:
        return message.parsed
    else:
        print("MESSAGE REFUSAL: ", message.refusal)
        return message.refusal