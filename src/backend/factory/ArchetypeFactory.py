from __future__ import annotations
from abc import ABC, abstractmethod
import json

# from langchain_openai import ChatOpenAI
from langchain_ollama.llms import OllamaLLM
from langchain_xai import ChatXAI

import src.backend.credentials as credentials


class Archetype(ABC):
    def set_llm(self, llm) -> None:
        match llm:
            case "ollama":
                self.llm_cool = OllamaLLM(model="clio")
                self.llm_hot = OllamaLLM(model="clio")
            case "xai":
                self.llm_cool = ChatXAI(
                    xai_api_key=credentials.XAI_API_KEY, model="grok-beta"
                )
                self.llm_hot = ChatXAI(
                    xai_api_key=credentials.XAI_API_KEY, model="grok-beta"
                )
            case _:
                self.llm_cool = OllamaLLM(model="clio")
                self.llm_hot = OllamaLLM(model="clio")

    @abstractmethod
    def set_prompt_templates(self) -> None:
        pass

    @abstractmethod
    def set_memory(self) -> None:
        pass

    @abstractmethod
    def set_chain(self, prompt_templates) -> None:
        pass

    def set_json_schema(self) -> None:
        self.json_schema = json.load(open("schema.json"))

    @abstractmethod
    def run_chain(self, query) -> None:
        pass


class ArchetypeFactory(ABC):
    @abstractmethod
    def build(self) -> None:
        pass

    def produce(self) -> Archetype:
        product = self.build()
        return product
