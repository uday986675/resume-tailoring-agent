from langgraph.graph import StateGraph, START, END
from state import ChatState
from utils import analyze_resume, analyze_jd, match_resume_to_jd, tailor_resume, evaluate_resume, revise_data

graph = StateGraph(ChatState)

graph.add_node('analyze_resume', analyze_resume)
graph.add_node('analyze_jd', analyze_jd)
graph.add_node('match_resume_to_jd', match_resume_to_jd)
graph.add_node('tailor_resume', tailor_resume)
graph.add_node('evaluate_resume', evaluate_resume)

graph.add_edge(START, 'analyze_resume')
graph.add_edge('analyze_resume', "analyze_jd")
graph.add_edge("analyze_jd", "match_resume_to_jd")
graph.add_edge('match_resume_to_jd', 'tailor_resume')
graph.add_edge('tailor_resume', 'evaluate_resume')

graph.add_conditional_edges(
    'evaluate_resume',
    revise_data,
    {
        'END' : END,
        'tailor_resume' : 'tailor_resume'
    }
)

workflow = graph.compile()

if __name__ == "__main__":
    intial_state = {
        "resume" : """
        # ARJUN KUMAR

**Software Engineer | AI/ML Enthusiast**

📧 [arjun.kumar.dev@example.com](mailto:arjun.kumar.dev@example.com)
📱 +91 98765 43210
🔗 linkedin.com/in/arjunkumar
🔗 github.com/arjunkumar

## PROFESSIONAL SUMMARY

Computer Science undergraduate with experience building AI-powered applications, machine learning systems, and backend services. Strong foundation in Python, data structures and algorithms, machine learning, and generative AI. Experienced in developing RAG applications, REST APIs, and agentic workflows using modern AI frameworks.

## EDUCATION

**B.Tech in Computer Science and Engineering**
ABC Institute of Technology, Andhra Pradesh
2023 – 2027
CGPA: 8.6/10

**Intermediate (MPC)**
XYZ Junior College, Andhra Pradesh
2021 – 2023
Percentage: 91.4%

## SKILLS

**Programming:** Python, Java, C++, SQL

**Machine Learning:** Scikit-learn, XGBoost, Pandas, NumPy, Matplotlib

**Deep Learning:** TensorFlow, Keras, CNN, LSTM, Transfer Learning

**Generative AI:** LangChain, LangGraph, RAG, FAISS, Prompt Engineering

**Web & Backend:** FastAPI, Flask, React.js, REST APIs

**Databases:** MySQL, PostgreSQL, MongoDB

**Tools:** Git, GitHub, Docker, VS Code, Jupyter Notebook

## PROJECTS

### AI Code Reviewer

**Python | LangGraph | LangChain | Groq API | FastAPI**

* Developed an AI-powered code review system capable of analyzing source code and identifying potential bugs, code quality issues, and improvement opportunities.
* Implemented a LangGraph workflow containing planner, coder, tester, and debugger nodes.
* Added tool-based file operations for reading, modifying, creating, and testing project files.
* Integrated automated testing and iterative debugging into the agent workflow.

### PDF Question Answering System

**Python | LangChain | FAISS | HuggingFace Embeddings**

* Built a Retrieval-Augmented Generation application that allows users to ask questions about uploaded PDF documents.
* Implemented document chunking, embedding generation, vector storage, and similarity-based retrieval.
* Used FAISS for efficient vector similarity search.
* Added conversational question answering using retrieved document context.

### Customer Churn Prediction

**Python | Scikit-learn | XGBoost | Pandas**

* Developed a machine learning model to predict customer churn using historical customer data.
* Performed data preprocessing, exploratory data analysis, feature engineering, and model evaluation.
* Compared multiple classification algorithms and selected XGBoost based on validation performance.
* Used SMOTE to address class imbalance.

### Stock Price Forecasting

**Python | SARIMAX | Pandas | Matplotlib**

* Built a time-series forecasting system for predicting stock prices using historical market data.
* Performed time-series preprocessing and model evaluation.
* Visualized historical and predicted values using Matplotlib.

## EXPERIENCE

### Machine Learning Intern

**TechVision Solutions Pvt. Ltd. — Hyderabad, India**
June 2026 – August 2026

* Developed preprocessing pipelines for customer datasets using Pandas and NumPy.
* Built classification models using Scikit-learn and XGBoost.
* Performed feature engineering and evaluated models using precision, recall, F1-score, and ROC-AUC.
* Collaborated with developers to expose trained models through REST APIs using FastAPI.
* Used Git and GitHub for version control and team collaboration.

### Open Source Contributor

**Independent**
January 2026 – Present

* Contributed bug fixes and documentation improvements to Python-based open-source projects.
* Reviewed pull requests and worked with Git-based development workflows.

## CERTIFICATIONS

**AI for Everyone: Master the Basics**
IBM Skills Network
2025

**Machine Learning with Python**
Coursera
2025

**Python Data Structures and Algorithms**
Udemy
2024

## ACHIEVEMENTS

* Solved 400+ problems on LeetCode.
* Participated in multiple university-level coding competitions.
* Ranked among the top performers in departmental programming contests.

""",
      "jd" : """
    # Software Engineer — AI/ML

**Company:** TechNova Labs
**Location:** Bengaluru, India
**Employment Type:** Full-time

## About the Role

TechNova Labs is looking for a **Software Engineer with a strong interest in Artificial Intelligence and Machine Learning** to join our engineering team.

The role involves developing backend services, machine learning applications, and AI-powered products. The ideal candidate should have strong Python programming skills, a good understanding of software engineering fundamentals, and practical experience building projects using machine learning or generative AI technologies.

## Responsibilities

* Design and develop scalable backend services and AI-powered applications using Python.
* Build data preprocessing and machine learning pipelines for real-world datasets.
* Develop and integrate REST APIs using FastAPI or Flask.
* Train, evaluate, and improve machine learning models using appropriate evaluation metrics.
* Implement feature engineering and data preprocessing workflows.
* Develop Retrieval-Augmented Generation applications using embeddings and vector databases.
* Experiment with Large Language Models and prompt engineering techniques.
* Build agentic workflows for AI-powered applications using modern AI frameworks.
* Write clean, maintainable, and well-tested code.
* Debug and troubleshoot software and machine learning pipelines.
* Collaborate with other engineers to integrate AI/ML components into production applications.
* Use Git and GitHub for source control and collaborative development.

## Required Skills

* Strong proficiency in Python.
* Good understanding of Data Structures and Algorithms.
* Strong understanding of machine learning fundamentals.
* Experience with Pandas and NumPy.
* Experience with Scikit-learn or similar machine learning frameworks.
* Knowledge of data preprocessing and feature engineering.
* Experience developing REST APIs.
* Familiarity with FastAPI or Flask.
* Knowledge of SQL and relational databases.
* Familiarity with Git and GitHub.
* Strong problem-solving and analytical skills.

## Preferred Skills

* Experience with TensorFlow or Keras.
* Experience with XGBoost.
* Experience with LangChain or LangGraph.
* Knowledge of Retrieval-Augmented Generation (RAG).
* Experience with FAISS or other vector databases.
* Knowledge of Large Language Models (LLMs).
* Experience with prompt engineering.
* Experience building AI agents or agentic workflows.
* Familiarity with Docker.
* Experience with cloud platforms such as AWS, Azure, or GCP.
* Experience with React.js or other frontend frameworks.

## Experience Requirements

Candidates with **0–2 years of relevant experience** in software engineering, machine learning, artificial intelligence, or a related field are preferred.

Strong academic projects, internships, open-source contributions, and demonstrable personal projects may be considered equivalent to professional experience.

## Qualifications

* Bachelor's degree or currently pursuing a Bachelor's degree in Computer Science, Information Technology, Artificial Intelligence, Data Science, or a related field.
* Strong understanding of computer science fundamentals.
* Ability to communicate technical concepts clearly.
* Demonstrated experience building software, machine learning, or AI projects.

## Keywords

Python, Software Engineering, Machine Learning, Artificial Intelligence, Data Structures, Algorithms, Pandas, NumPy, Scikit-learn, Data Preprocessing, Feature Engineering, REST API, FastAPI, Flask, SQL, Git, GitHub, TensorFlow, Keras, XGBoost, LangChain, LangGraph, RAG, FAISS, Vector Database, LLM, Prompt Engineering, AI Agents, Agentic Workflows, Docker, AWS, Azure, GCP, React.js, Backend Development, Model Evaluation, Machine Learning Pipelines.

"""  
    }

    response = workflow.invoke(intial_state)

    print(response.get('resume_data'))
    print('==' * 50)
    print(response.get('tailored_resume'))
    print('==' * 50)
    print(response.get('evaluated_data'))
    # print('==' * 50)
    # print(response.get('match_data'))