from pydantic import BaseModel
from typing import List

class ResumeAnalyzerSchema(BaseModel):
    skills : List[str]
    education : List[dict]
    projects : List[dict]
    experience : List[dict]
    certifications : List[dict]

class JDSchema(BaseModel):
    job_title : str
    company : str
    required_skills : List[str]
    preferred_skills : List[str]
    responsibilities : List[str]
    experience_requirements : List[str]
    qualifications : List[str]
    keywords : List[str]

class SkillMatch(BaseModel):
    skill : str
    reason : str

class MatchSchema(BaseModel):
    strong_matches : List[SkillMatch]
    partial_matches : List[SkillMatch]
    missing_skills : List[str]

    match_score : float
    explanation : str

class EvaluatorSchema(BaseModel):
    ATS_score : int
    content_score : int
    Truthfulness_check : int

    passed : bool
    issues : List[str]
    suggestions : List[str]



