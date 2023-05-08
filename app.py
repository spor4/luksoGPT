# app.py

import os
#from config import APIKEYGITHUB
#from config import APIKEYOPENAI


import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from github_api_wrapper import GitHubAPIWrapper

# Set the OpenAI API key from your apikey file
os.environ['OPENAI_API_KEY'] = st.secrets["APIKEYOPENAI"]

# App framework
st.title('Why is LUKSO awesome? 🆙')

# Initialize GitHub API
github_api = GitHubAPIWrapper(api_token = st.secrets["APIKEYGITHUB"])

# Get repository and subdirectory information
repo_infos = [
    {
        "owner": "lukso-network",
        "repo": "LIPs",
        "subdir": "LSPs",
    },
    {
        "owner": "lukso-network",
        "repo": "LIPs",
    },
]

repo_details = []
for repo_info in repo_infos:
    repo_data = github_api.get_repo_info(repo_info["owner"], repo_info["repo"], subdir=repo_info.get("subdir"))
    repo_details.append(repo_data)

# Prompt template
question_template = PromptTemplate(
    input_variables=["question", "repo_details"],
    template="Answer the following question about the GitHub repositories: {question}\n\n"
              "Repository details:\n{repo_details}"
)




# Memory
question_memory = ConversationBufferMemory(input_key="question", memory_key="chat_history")







# LLMs
llm = OpenAI(temperature=0.9)
question_chain = LLMChain(llm=llm, prompt=question_template, verbose=True, output_key="answer", memory=question_memory)

question = st.text_input("Ask a question about LUKSOs LSPs.")

# Show the answer if there's a question
if question:
    formatted_repo_details = "\n\n".join([f"{'-' * 10}\n" + "\n".join([f"{k}: {v}" for k, v in repo.items()]) if isinstance(repo, dict) else "\n".join([f"{item['name']}" for item in repo]) for repo in repo_details])
    answer = question_chain.run(question=question, repo_details=formatted_repo_details)

    st.write(answer)

    with st.expander("Answer History"):
        st.info(question_memory.buffer)
