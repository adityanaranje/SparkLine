import streamlit as st
from services.auth import Auth
from components.login import LoginPage
import time
from services.utils import Operation
from services.pdf import Pdffile
from services.activity import ActivityLogger
import os
import pandas as pd
import base64

authenticate = Auth()
login_page = LoginPage(authenticate)
response = Operation()
pdffile = Pdffile()
active = ActivityLogger()

st.set_page_config(page_title="SparkLine", page_icon="🤖")

# Set background of api
bg = "static/images/background.jpg"
bg_ext = "jpg"

# Encode the image
with open(bg, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode()

# Inject updated CSS
st.markdown(
    f"""
    <style>
    html, body, [data-testid="stApp"] {{
        background-image: url("data:image/{bg_ext};base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("SparkLine")
st.sidebar.title("SparkLine")
st.sidebar.image("static/images/sidebar.jpg")



with open("static/files/SampleResume.pdf", "rb") as f:
    sample_pdf = f.read()

def stream_data(data):
    for word in data.split(" "):
        yield word + " "
        time.sleep(0.05)

def main():
    # Setup session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False


    if not st.session_state.logged_in:
        is_user_valid, logged_user = login_page.login_user()

        # If login attempted (True/False)
        if is_user_valid is not None:
            if is_user_valid:
                st.session_state.logged_in = True
                st.session_state.logged_user = logged_user
                st.rerun()
            else:
                st.error("❌ Invalid login credentials.")
        return


    

    # Logout button
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    username = st.session_state.get("logged_user", "UnknownUser")

    if username == "AdityaNaranje":
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Outreach", "JD Match", "Q&A Prep", "PrepWeek", "YourActivity","Contact","All Activities"])
    else:
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Outreach", "JD Match", "Q&A Prep", "PrepWeek","YourActivity","Contact"])

    with tab1:
        st.write_stream(stream_data("##### Craft a professional cold email tailored to the job description."))
       
        col1, col2, col3 = st.columns(3)

        with col1:
            user_name = st.text_input("Your Name", key="user_name")
        with col2:
            user_designation = st.text_input("Your Designation", key="user_designation")
        with col3:
            user_company = st.text_input("Your Company Name", key="user_company")

        col5, col6 = st.columns([3,1])
        with col5:
            job_link = st.text_input("Enter job link",key="job_link1", value="https://careers.nike.com/software-engineer-ii-itc/job/R-65543")
        with col6:
            user_experience = st.selectbox("Your Experience", ["0-1 Year","1-3 Years","3-5 Years","5-7 Years","7-10 Years","10-15 Years","15+ Years"])
        
        
        if st.button("Generate", key="btn1"):
            if response.is_valid_url(job_link):
                if user_name and user_designation and user_company and job_link:
                    with st.spinner("Generating....."):
                        res = response.get_job(job_link)
                        mail = response.get_email(res, user_name, user_designation, user_company, user_experience)              
                    cleaned_lines = [
                        line for line in mail.strip().split("\n") # type: ignore
                        if not line.strip().lower().startswith("here is")
                    ]

                    cleaned_email = "\n".join(cleaned_lines) 

                    st.toast("Generated", icon="🎉")              
                    st.markdown(cleaned_email)


                    username = st.session_state.get("logged_user", "UnknownUser")
                    
                    active.log_activity(username=username, tab="Cold Email")

                    file_path = f'static/responses/coldmails/{username}ColdMail.pdf'

                    pdffile.save_markdown_as_pdf(text = cleaned_email, file_path=file_path) # type: ignore

                    if os.path.exists(file_path):
                        with open(file_path, "rb") as f:
                            pdf_data = f.read()

                        st.download_button(
                            label="📥 Download Cold Email",
                            data=pdf_data,
                            file_name="ColdMail.pdf",
                            mime="application/pdf"
                        )

                else:
                    st.error("Please enter data")
            else:
                st.error("❌ Link is not valid or unreachable")

    with tab2:
        st.write_stream(stream_data("##### Analyze your resume against the job and see what to improve."))
        
        
        job_link = st.text_input("Enter job link", key="job_link2", value="https://careers.nike.com/software-engineer-ii-itc/job/R-65543")

        candidate_resume = st.file_uploader("Upload Resume", key="file2", type="pdf")

        col1, col2, col3 = st.columns([1,2,1])
        with col1:
            btn2 =  st.button("Generate",key="btn2")
        
        with col3:
            st.download_button(label="Download Sample",key="sample2",data=sample_pdf,file_name="sample.pdf",mime="application/pdf")
            
        if btn2:
            if response.is_valid_url(job_link):
                if candidate_resume and job_link:
                    username = st.session_state.get("logged_user", "UnknownUser")
                    file_path = f'static/files/resumes/{username}Resume.pdf'

                    active.log_activity(username=username, tab="JD Match")
                    with open(file_path, "wb") as f:
                        f.write(candidate_resume.getbuffer())

                    with st.spinner("Generating....."):
                        job_data = response.get_job(job_link)
                        resume_data = response.fetch_resume(file_path)
                        output_content = response.jd_match(job_data=job_data, resume_data=resume_data)
                    st.toast("Generated", icon="🎉")
                    st.markdown(output_content)


                    file_path = f'static/responses/matches/{username}PlanOutput.pdf'
                    pdffile.save_markdown_as_pdf(text = output_content, file_path=file_path) # type: ignore

                    if os.path.exists(file_path):
                        with open(file_path, "rb") as f:
                            pdf_data = f.read()

                        st.download_button(
                            label="📥 Download Match",
                            data=pdf_data,
                            file_name="JdMatch.pdf",
                            mime="application/pdf"
                        )


                else:
                    st.error("Please enter data")
            else:
                st.error("❌ Link is not valid or unreachable")

    with tab3:
        st.write_stream(stream_data("##### Get interview questions and ideal answers based on your profile."))
        job_link = st.text_input("Enter job link", key="job_link3", value="https://careers.nike.com/software-engineer-ii-itc/job/R-65543")

        candidate_resume = st.file_uploader("Upload Resume", key="file3",type="pdf")

        col1, col2, col3 = st.columns([1,2,1])
        
        with col1:
            btn3 =  st.button("Generate",key="btn3")
        
        with col3:
            st.download_button(label="Download Sample",key="sample3",data=sample_pdf,file_name="sample.pdf",mime="application/pdf")

        if btn3:
            if response.is_valid_url(job_link):
                if candidate_resume and job_link:
                    username = st.session_state.get("logged_user", "UnknownUser")
                    file_path = f'static/files/resumes/{username}Resume.pdf'
                    active.log_activity(username=username, tab="Interview Questions")
                   
                    with open(file_path, "wb") as f:
                        f.write(candidate_resume.getbuffer())

                    with st.spinner("Generating....."):
                        job_data = response.get_job(job_link)
                        resume_data = response.fetch_resume(file_path)
                        output_content = response.get_interview_ques(job_data=job_data, resume_data=resume_data)
                    
                    # Store in session_state
                    st.session_state.interview_output = output_content
                    st.toast("Generated", icon="🎉")
            else:
                st.error("❌ Link is not valid or unreachable")
                

        if "interview_output" in st.session_state and response.is_valid_url(job_link):
            output_content = st.session_state.interview_output
            with st.expander("See Questions..."):
                st.markdown("### 🎯 Interview Questions:")
                for category, questions in output_content["questions"].items():
                    st.markdown(f"#### {category.capitalize()} Questions")
                    for i, question in enumerate(questions, 1):
                        st.markdown(f"- {question}")

            
            if st.button("Get Answers", key="btn3_2"):
                role = output_content["role"]
                questions = output_content["questions"]
                
                with st.spinner("Generating Answers..."):
                    output_answers = response.get_interview_ans(role=role, questions=questions)

                st.toast("Generated", icon="🎉")
                st.session_state.interview_answers = output_answers
                with st.expander("See Answers"):
                    st.markdown(output_answers)

                username = st.session_state.get("logged_user", "UnknownUser")
                file_path = f'static/responses/answers/{username}AnswerOutput.pdf'
                pdffile.save_markdown_as_pdf(text = output_answers, file_path=file_path) # type: ignore

                active.log_activity(username=username, tab="Interview Answers")
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        pdf_data = f.read()

                    st.download_button(
                        label="📥 Download Answers",
                        data=pdf_data,
                        file_name="interviewquesans.pdf",
                        mime="application/pdf"
                    )

    with tab4:
        st.write_stream(stream_data("##### Personalized 7-day study plan to prepare before your interview."))
        job_link = st.text_input("Enter job link", key="job_link4", value="https://careers.nike.com/software-engineer-ii-itc/job/R-65543")

        candidate_resume = st.file_uploader("Upload Resume", key="file4",type="pdf",)

        col1, col2, col3 = st.columns([1,2,1])

        with col1:
            btn4 = st.button("Generate",key="btn4")
        
        
        with col3:
            st.download_button(label="Download Sample",key="sample4",data=sample_pdf,file_name="sample.pdf",mime="application/pdf")

        if btn4:
            if response.is_valid_url(job_link):
                if candidate_resume and job_link:
                    username = st.session_state.get("logged_user", "UnknownUser")
                    file_path = f'static/files/resumes/{username}Resume.pdf'

                    active.log_activity(username=username, tab="7 Days Plan")
                    with open(file_path, "wb") as f:
                        f.write(candidate_resume.getbuffer())

                    with st.spinner("Generating....."):
                        job_data = response.get_job(job_link)
                        resume_data = response.fetch_resume(file_path)
                        output_plan = response.get_prep_plan(job_data=job_data, resume_data=resume_data)
                    
                    st.toast("Generated", icon="🎉")
                    st.markdown(output_plan)

                    file_path = f'static/responses/plans/{username}PlanOutput.pdf'
                    pdffile.save_markdown_as_pdf(text = output_plan, file_path=file_path) # type: ignore

                    if os.path.exists(file_path):
                        with open(file_path, "rb") as f:
                            pdf_data = f.read()

                        st.download_button(
                            label="📥 Download 7-Day Plan",
                            data=pdf_data,
                            file_name="plan.pdf",
                            mime="application/pdf"
                        )
            else:
                st.error("❌ Link is not valid or unreachable")
    with tab5:
        username = st.session_state.get("logged_user", "UnknownUser")
        data = active.get_logs_by_user(username=username)
        df = pd.DataFrame(data, columns = ["UserName", "Activity","Time"])
        if df.shape[0]==0:
            st.info("No Activity")
        else:
            st.table(df)

    with tab6:
        st.markdown("### 🌐 Connect with me")

        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

        with col1:
            st.markdown('[![LinkedIn](https://img.shields.io/badge/-LinkedIn-blue?logo=linkedin&style=flat)](https://www.linkedin.com/in/anaranje)', unsafe_allow_html=True)

        with col2:
            st.markdown('[![GitHub](https://img.shields.io/badge/-GitHub-black?logo=github&style=flat)](https://github.com/adityanaranje)', unsafe_allow_html=True)

        with col3:
            st.markdown('[![Instagram](https://img.shields.io/badge/-Instagram-E4405F?logo=instagram&style=flat)](https://www.instagram.com/aditya.naranje7/)', unsafe_allow_html=True)

        with col4:
            st.markdown('[![Email](https://img.shields.io/badge/-Email-D14836?logo=gmail&style=flat)](mailto:aditya.naranje7@gmail.com)', unsafe_allow_html=True)

        with col5:
            st.markdown('[![Medium](https://img.shields.io/badge/-Medium-00ab6c?logo=medium&style=flat)](https://adityanaranje.medium.com/)', unsafe_allow_html=True)

        with col6:
            st.markdown('[![Kaggle](https://img.shields.io/badge/-Kaggle-20BEFF?logo=kaggle&style=flat)](https://www.kaggle.com/adityanaranje)', unsafe_allow_html=True)

        with col7:
            st.markdown('[![Portfolio](https://img.shields.io/badge/-Portfolio-lightgrey?logo=firefoxbrowser&style=flat)](https://adityanaranje.github.io/MY-PORTFOLIO/)', unsafe_allow_html=True)


    if username == "AdityaNaranje":
        with tab7: # type: ignore
            data = active.get_all_logs()
            df = pd.DataFrame(data, columns = ["Id","UserName", "Activity","Time"])
            if df.shape[0]==0:
                st.info("No Activity")
            else:
                st.table(df)

if __name__ == '__main__':
    main()

