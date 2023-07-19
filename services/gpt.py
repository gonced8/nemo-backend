import openai
import os
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt
from typing import List, Tuple, Union
from agents import OnboardingValue
openai.organization = os.getenv("OpenAI-Organization")
openai.api_key = os.getenv("OPENAI_API_KEY")

class GPT:
    
    def __init__(
        self,
        prompt_template: str = "",
        openai_model: str = "gpt-3.5-turbo",
        api_org: str = None,
        api_key: str = None,
    ):
        self.openai_model = openai_model
        
        
    @retry(stop=stop_after_attempt(10))
    def chat_completion(self,
        messages: list,
        agent: OnboardingValue,
        n_samples: int = 1,
        temperature: float = 0.3,
        top_p: float = 1.0,
        max_tokens=1024,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0
    ):

        messages = self.messages_to_prompt(messages)
        
        openai_args = {
            "model": self.openai_model,
            "messages": messages,
            "temperature": temperature,
            "n": n_samples,
            "top_p": top_p,
            "max_tokens": max_tokens,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
        }

        response = openai.ChatCompletion.create(**openai_args)
        return response["choices"][0]["message"]["content"]
        
        
        def messages_to_prompt(messages:list):
        # Messages to prompt with roles
        # recover messages from database
            pass