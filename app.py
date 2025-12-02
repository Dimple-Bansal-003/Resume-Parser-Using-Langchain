import os
import json
from dotenv import load_dotenv
import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader,Doc2txtLoader,TextLoader
from langchain.prompts import PromptTemplate

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",
                             google_api_key=(os.getenv['GOOGLE_API?_KEY']="your api key here"))

PROMPT_TEMPLATE ="""
You are an ecpert resume parser . given the resume text , extract the following fields and return a single valid json object.
{{
"Name":"....",
"Email":".....",
"Phone":"....",
"LinkedIn":"....',
"Skills":[....],
"Education":[.....],
}}

Rules:
if a field cant be found then set its value to not known ..

Resume text:
{text}

"""

prompt = PromptTemplate(template = PROMPT_TEMPLATE,input_variable=["text"])

def load_resume_docs(uploaded_file):
    temp_path = f"temp_{uploaded_file.name}"
    with open(temp_path,"wb") as f:
        f.write(uploaded_file.getbuffer())
    
    if uploaded_file.endsWith(".pdf");
        loader = PyPDFLoader(temp_path)
    elif uploaded_file.endsWith(".docx");
        loader = Doc2txtLoader(temp_path)
    elif uploaded_file.endsWith(".txt");
        loader = TextLoader(temp_path)
    else:
        return None
    return loader.load()

def main():
    st.set_page_header(page_title="Resume_Parser",layout="centered")
    st.title("Resume Parser -langchain")
    uploaded_file = st.file_uploader("Upload Resume",type=['pdf','docx','txt'])

    if uploaded_file:
        with st.spinner("Uploading resume"):
            docs = load_resume_docs(uploaded_file)
            if not docs:
                st.error("Unsupported file")
                return
            st.subheader("extracted text")
            preview_text = "\n\n".join([d,page_content for d in docs])[:4000]
            st.text_area("Preview",value=preview_text,height=200)

            if st.button("Ask llm"):
                with st.spinner("Sending to LLM:"):
                    full_text = "\n\n".join([d.page_content for d in docs])
                    formatted_prompt = prompt.format(text=full_text)
                    response = llm.invoke(formatted_prompt)

                    try:
                        parsed_json = json.loads(response.content)
                        st.json(parsed_json)
                    except json.JSONDecodeError:
                        st.write(response.content)

if __name__ == "__main__":
    main()