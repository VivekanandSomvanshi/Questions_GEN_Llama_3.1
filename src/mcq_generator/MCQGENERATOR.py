import os
import json
from datetime import datetime, timedelta
import traceback

import pandas as pd
from dotenv import load_dotenv

from groq import Groq
from langchain.chains import LLMChain, SequentialChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.agents import AgentType, load_tools, initialize_agent
from langchain.callbacks import get_openai_callback
from langchain.schema import HumanMessage, AIMessage, ChatMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

load_dotenv()

KEY = os.getenv('GROQ_API_KEY')

groq_chat = ChatGroq(groq_api_key=KEY, model_name="llama3-70b-8192",temperature=0.5)

TEMPLATE="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}

"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=TEMPLATE
    )

quiz_chain=LLMChain(llm=groq_chat, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)

TEMPLATE_1="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis.
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", "quiz"], template=TEMPLATE_1)

review_chain=LLMChain(llm=groq_chat, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

# This is an Overall Chain where we run the two chains in Sequence

generate_evaluate_chain=SequentialChain(chains=[quiz_chain, review_chain], input_variables=["text", "number", "subject", "tone", "response_json"],
                                        output_variables=["quiz", "review"], verbose=True,)