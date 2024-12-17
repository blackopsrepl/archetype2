from langchain.schema import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda

from operator import itemgetter

from src.backend.factory.ArchetypeFactory import Archetype, ArchetypeFactory
import src.backend.factory.prompt_templates as prompt_templates


class TaskEvaluator(Archetype):
    def set_prompt_templates(self) -> None:
        self.t = prompt_templates.task_evaluator

    def set_memory(self) -> None:
        self.memory = ConversationBufferMemory(return_messages=True)
        self.memory.load_memory_variables({})

    def set_chain(self) -> None:
        self.task_evaluator_chain = (
            RunnablePassthrough.assign(
                memory=RunnableLambda(self.memory.load_memory_variables)
                | itemgetter("history")
            )
            | self.t["evaluate_template"]
            | self.llm_cool
            | StrOutputParser()
        )

    def run_chain(self, user_query) -> str:
        task = self.task_evaluator_chain.invoke({"text": user_query})
        return task


class TaskEvaluatorFactory(ArchetypeFactory):
    def build(self, llm) -> Archetype:
        self.task_evaluator = TaskEvaluator()
        self.task_evaluator.set_llm(llm)
        self.task_evaluator.set_prompt_templates()
        self.task_evaluator.set_memory()
        self.task_evaluator.set_chain()
        return self.task_evaluator
