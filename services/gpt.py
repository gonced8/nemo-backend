import os

import openai
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt

# Load .env file
load_dotenv()

openai.organization = os.getenv("OPENAI_API_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")


class GPT:
    def __init__(
        self,
        openai_model: str = "gpt-3.5-turbo",
    ):
        self.openai_model = openai_model

    @retry(stop=stop_after_attempt(10))
    def chat_completion(
        self,
        messages: list,
        n_samples: int = 1,
        temperature: float = 0.3,
        top_p: float = 0.9,
        max_tokens=1024,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
    ) -> str:
        openai_args = {
            "model": self.openai_model,
            "messages": self.messages_to_prompt(messages),
            "temperature": temperature,
            "n": n_samples,
            "top_p": top_p,
            "max_tokens": max_tokens,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
        }

        response = openai.ChatCompletion.create(**openai_args)
        return response["choices"][0]["message"]["content"]

    def messages_to_prompt(
        self, messages: list[tuple[str, str]]
    ) -> list[dict[str, str]]:
        # Messages to prompt with roles
        return [{"role": role, "content": content} for role, content in messages]
