from langchain.schema import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda

from operator import itemgetter

from src.backend.factory.ArchetypeFactory import Archetype, ArchetypeFactory
import src.backend.factory.prompt_templates as prompt_templates


class EssayComposer(Archetype):
    def set_prompt_templates(self) -> None:
        self.t = prompt_templates.essay_composer

    def set_memory(self) -> None:
        self.memory = ConversationBufferMemory(return_messages=True)
        self.memory.load_memory_variables({})

    def set_chain(self) -> None:
        self.subtopics_chain = (
            RunnablePassthrough.assign(
                memory=RunnableLambda(self.memory.load_memory_variables)
                | itemgetter("history")
            )
            | self.t["subtopics_template"]
            | self.llm_cool
            | StrOutputParser()
        )
        self.axes_chain = (
            RunnablePassthrough.assign(
                memory=RunnableLambda(self.memory.load_memory_variables)
                | itemgetter("history")
            )
            | self.t["axes_template"]
            | self.llm_cool
            | StrOutputParser()
        )
        self.outline_chain = (
            RunnablePassthrough.assign(
                memory=RunnableLambda(self.memory.load_memory_variables)
                | itemgetter("history")
            )
            | self.t["outline_template"]
            | self.llm_hot
            | StrOutputParser()
        )

    def run_chain(self, user_query) -> str:
        subtopics = self.subtopics_chain.invoke({"topic": user_query})
        axes = self.axes_chain.invoke({"subtopics": subtopics})
        outline = self.outline_chain.invoke(
            {"topic": user_query, "subtopics": subtopics, "axes": axes}
        )
        return outline


class EssayComposerFactory(ArchetypeFactory):
    def build(self, llm) -> Archetype:
        self.essay_planner = EssayComposer()
        self.essay_planner.set_llm(llm)
        self.essay_planner.set_prompt_templates()
        self.essay_planner.set_memory()
        self.essay_planner.set_chain()
        return self.essay_planner
