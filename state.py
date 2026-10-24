from typing import TypedDict
from schemas import ResumeAnalyzerSchema, JDSchema, MatchSchema, EvaluatorSchema

class ChatState(TypedDict):
    resume : str
    jd : str

    resume_data : ResumeAnalyzerSchema
    jd_data : JDSchema
    match_data : MatchSchema

    tailored_resume : str

    evaluated_data : EvaluatorSchema

    revision_count : int