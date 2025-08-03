from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import JsonOutputParser
from langchain_community.document_loaders import PyPDFLoader
from services.chains import Chain
import requests

chains = Chain()
json_parser = JsonOutputParser()

class Operation:
    def is_valid_url(self, url):
        try:
            response = requests.head(url, allow_redirects=True, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def get_job(self, job_link):
        loader = WebBaseLoader(job_link)
        job_data = loader.load().pop().page_content
        chain = chains.job_extract()
        res = chain.invoke({"job_data":job_data})
        
        json_res = json_parser.parse(res.content) # type: ignore
        
        return str(json_res) 
    
    def get_email(self,job_description, user_name, user_designation,user_company ,user_experience):
        chain = chains.generate_email()
        res = chain.invoke({"job_description":job_description,
                                "user_name":user_name,
                                "user_designation":user_designation,
                                "user_company":user_company,
                                "user_experience":user_experience})
        return res.content
    
    def fetch_resume(self, candidate_resume):
        loader = PyPDFLoader(candidate_resume)
        docs = loader.load()
        resume_text = "\n\n".join([page.page_content for page in docs])
        chain = chains.extract_resume()
        res = chain.invoke(input = {"pdf_data":resume_text})
        json_res = json_parser.parse(res.content) # type: ignore
        
        return json_res
    
    def jd_match(self, job_data, resume_data):
        chain = chains.job_desc_match()
        res = chain.invoke({"job_data":job_data, "resume_data":resume_data})
        return res.content

    def get_interview_ques(self, job_data, resume_data):
        chain = chains.interview_prep()
        res = chain.invoke({"job_data":job_data, "resume_data":resume_data})
        json_res = json_parser.parse(res.content) # type: ignore
        return json_res
    
    def get_interview_ans(self, role, questions):
        chain = chains.question_answers()
        res = chain.invoke({"role":role, "questions":questions})
        return res.content
    
    def get_prep_plan(self, job_data, resume_data):
        chain = chains.prep_plan()
        res = chain.invoke({"job_data":job_data, "resume_data":resume_data})
        return res.content