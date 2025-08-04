# 💼 Job Assistant Streamlit App

A powerful **Streamlit-based Job Assistant** to help candidates streamline their job search. Using AI and a single job link + resume, this app can generate:

- ✉️ Cold emails to hiring managers  
- 🔍 Resume ↔ Job Description Matching  
- 🎯 AI-generated mock interview questions  
- 📅 Personalized 7-day preparation plan  

---

## 🌐 Live App

👉 [Click here to try the app](https://sparkline-aditya-naranje.streamlit.app/)

> No installation required — just open the link, upload your resume, and paste a job description link!

---

## 🧪 Sample Job Links
Try the app with these sample job listings:

- [Job Link 1](https://careers.nike.com/software-engineer-ii-itc/job/R-65543)
- [Job Link 2](https://southasiacareers.deloitte.com/job/Mumbai-Technology-and-Transformation-EAD-AI-&-Data-Senior-Consultant-Gen-AI/42961144/)
- [Job Link 3](https://southasiacareers.deloitte.com/job/Bengaluru-T&T-Engineering-ADMM-Consultant-Tableau/41512244/)
- [Job Link 4](https://southasiacareers.deloitte.com/job/Bengaluru-Eco-space-T&T-Engineering-PDI-Senior-Consultant-Java/41510944/)
- [Job Link 5](https://southasiacareers.deloitte.com/job/Mumbai-ConsultantSenior-Consultant-Azure-Database-for-MySQL-Mumbai-Engineering/39830844/)
- [Job Link 6](https://southasiacareers.deloitte.com/job/Delhi-T&T-EAD-OIDS-Consultant-UIUX-Developer-Delhi/40825744/)
- [Job Link 7](https://southasiacareers.deloitte.com/job/Bengaluru-T&T-EAD-OIDS-Consultant-API-Developer-Bengaluru-Operations%2C-Industry-&-Domain-Solutions/43295244/)

## 🚀 Features

🔹 **Input** a job link and upload your resume (PDF)  
🔹 **Generate** tailored cold outreach email  
🔹 **Match** your resume with JD to highlight gaps & alignment  
🔹 **Practice** with auto-generated mock interview questions  
🔹 **Plan** your next 7 days of preparation using personalized insights  
🔹 **User-friendly interface** built with Streamlit  

---

## 🧰 Tech Stack

| Layer        | Tech Used                                               |
|--------------|----------------------------------------------------------|
| Frontend     | Streamlit                                                |
| Backend      | LangChain + Groq (LLM interface)                         |
| Parsing      | BeautifulSoup, PDF to text, base64 for file handling     |
| Persistence  | SQLite (via `pysqlite3-binary`)                          |
| PDF Export   | xhtml2pdf                                                |
| LLM Tasks    | LangChain Core + Community integrations                  |

---

## 📦 Dependencies

Install all dependencies with:

```bash
pip install -r requirements.txt
