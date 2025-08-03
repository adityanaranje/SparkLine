from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
my_key = st.secrets["api_keys"]["groqapi"]



class Chain:
    def __init__(self):
        self.llm = ChatGroq(model = "llama3-70b-8192", 
                            groq_api_key = my_key,  # type: ignore
                            temperature=0)
        
    def job_extract(self):
        job_extract_prompt = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE
            {job_data}
            ### INSTRUCTION
            The scraped text is from the careers's page of a website.
            Your job is to extract the job postings and return them in json format containing following keys: `role`, `experience`,`skills` and `description`
            Only return the valid json NO PREAMBLE.
            ### VALID JSON (NO PREAMBLE):
            """
            )
        job_extract_chain = job_extract_prompt | self.llm
        return job_extract_chain
    
    def generate_email(self):
        email_prompt = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION
            {job_description}
            ### INSTRUCTION:
            You are {user_name}, a {user_designation} at {user_company} having {user_experience} of experience.     
            Your job is to write a cold email to the client regarding the job mentioned above describing the capability of me
            in fulfilling their needs.
            Also add two sample project links with it's technology/skills.
            Remember you are {user_name}, {user_designation} at {user_company}.
            At last write 
            {user_name}, \n
            {user_designation}, {user_company}
            Do not provide a preamble.
            Remember no not include preamble like here is the cold email.
            ### EMAIL (NO PREAMBLE):
            """
        )
        generate_email_chain = email_prompt | self.llm
        return generate_email_chain
    
    def extract_resume(self):
        resume_prompt = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM RESUME PDF
            {pdf_data}
            ### INSTRUCTION
            The scraped text is from the candidates resume page of a pdf.
            You are an expert resume analyzer.
            Your job is to extract the details and return them in json format containing following keys: `candidate details`,`education` ,`experience`,`skills`, `projects`,`tasks` and `certification` with links if present any
            Please ignore if anything is not present.
            Only return the valid json NO PREAMBLE.
            ### VALID JSON (NO PREAMBLE):
            """
        )

        chain_extract = resume_prompt | self.llm
        return chain_extract
    
    def job_desc_match(self):
        jd_match_prompt = PromptTemplate.from_template (
                """
                You are an experienced technical recruiter. Analyze the candidate’s resume against the job description below and explaing directly to candidate.
                
                ### Job Description:
                {job_data}
                
                ### Candidate Resume:
                {resume_data}
                
                Evaluate how well the candidate matches the job. Provide:
                
                1.  **Strengths**: Skills, experience, or qualifications that align well.
                2.  **Gaps**: Missing or weak areas in skills or qualifications.
                3.  **Overall Fit rate** (out of 10) with a brief justification.
                
                Be concise but thorough and write as you are explaining directly to candidate. Use bullet points. 
                Please remove any preamble if present.
                Don't add any closings
                """
        )
        jd_match_chain = jd_match_prompt | self.llm
        return jd_match_chain
    
    def interview_prep(self):
        interview_prep_prompt = PromptTemplate.from_template(
            """
            You are an experienced interviewer preparing a mock interview based on the job description and the candidate’s resume.

            ## Job Description:
            {job_data}

            ## Candidate Resume:
            {resume_data}

            Your task:
            Generate a realistic set of **interview questions only**, organized into the following sections:

            1. **Technical Questions**  
            - Based on technologies, frameworks, or domain expertise mentioned in the JD.  
            - Focus on core skills, architecture, and problem-solving.

            2. **Coding Questions** (only if relevant)  
            - Include 2-3 coding problems based on the job requirements.  
            - Cover time/space complexity, edge cases, or API/system design.

            3. **Managerial / Behavioral Questions**  
            - Based on the candidate’s experience and the responsibilities in the JD.  
            - Include topics like leadership, ownership, collaboration, and deadlines.

            4. **HR / Cultural Fit Questions**  
            - Assess motivation, adaptability, values alignment, and long-term goals.

            ## Guidelines:
            - Do **not** include answers, explanations, or preambles.
            - Phrase each question as if being asked in a real interview.
            - Focus on relevance and clarity.

            ## Output Format:
            Return a **JSON object** with the following structure:

            
            {{
            "role": "Job Role Title",
            "questions": {{
                "technical": ["Question 1", "Question 2", "..."],
                "coding": ["Question 1", "Question 2", "..."],
                "managerial": ["Question 1", "Question 2", "..."],
                "hr": ["Question 1", "Question 2", "..."]
            }}
            }}
            ```

            All questions should be properly formatted in **Markdown** within the strings.

            Only output the JSON. Do not include commentary, markdown blocks, or prose.
            """
        )

        interview_prep_chain = interview_prep_prompt | self.llm
        return interview_prep_chain
    
    def question_answers(self):
        interview_ans_prompt = PromptTemplate.from_template(
            """
            You are an expert {role}.

            ## Questions:
            {questions}

            ## Task:
            Generate ideal answers for the above set of interview questions.

            - Write all answers in **Markdown format**, paired with their questions.
            - Use appropriate markdown formatting for any code, logic, or mathematical content.
            - Keep answers clear, concise, and technically accurate.
            - Do **not** include any introductory or closing remarks.

            ## Output Format:
            - Use clear section subheadings if applicable.
            - Number each question and answer pair.

            Begin only with the answers.
            """
        )

        interview_ans_chain = interview_ans_prompt | self.llm
        return interview_ans_chain
    
    def prep_plan(self):
        prep_plan_prompt = PromptTemplate.from_template(
            """
            You are an expert career coach. Create a personalized 7-day revision plan for a candidate preparing for a job interview.
            
            ## Job Description:
            {job_data}
            
            ## Candidate Resume:
            {resume_data}
            
            ## Instructions:
            - Identify the key topics/technologies from the job.
            - Evaluate where the candidate needs focus (based on resume).
            - Create a **7-day schedule** including what to study or practice each day.
            - Add suggested resources (e.g. websites, topics to search, mock tasks).
            
            Format the output clearly using day-wise headings (Day 1, Day 2, etc.).

            """
        )
        prep_plan_chain = prep_plan_prompt | self.llm
        return prep_plan_chain


    

