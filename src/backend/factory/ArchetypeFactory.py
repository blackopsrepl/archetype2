from __future__ import annotations
from abc import ABC, abstractmethod
import json


class Archetype(ABC):
    @abstractmethod
    def set_llm(self) -> None:
        pass

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
