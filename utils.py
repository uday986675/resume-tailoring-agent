from typing import TypeVar
from pydantic import BaseModel
import re
import json

from state import ChatState
from model import getModel
from prompts import (
    RESUME_ANALYZER_PROMPT, 
    JD_ANALYZER_PROMPT, 
    MATCH_ANALYZER_PROMPT, 
    TAILOR_RESUME_PROMPT, 
    EVALUATION_PROMPT
)
from schemas import ResumeAnalyzerSchema, JDSchema, MatchSchema, EvaluatorSchema

# We no longer need invoke_structured, json, or TypeVar.
# GeminiSafe handles all the JSON parsing, truncation repair, and validation natively.

def analyze_resume(state: ChatState):
    resume = state['resume']
    model = getModel()
    
    # Native structured output - GeminiSafe will intercept and repair here
    structured_model = model.with_structured_output(ResumeAnalyzerSchema)
    prompt = RESUME_ANALYZER_PROMPT.format(resume=resume)

    response = structured_model.invoke(prompt)
    return {"resume_data": response}


def analyze_jd(state: ChatState):
    jd = state['jd']
    model = getModel()
    
    structured_model = model.with_structured_output(JDSchema)
    prompt = JD_ANALYZER_PROMPT.format(job_description=jd)

    response = structured_model.invoke(prompt)
    return {"jd_data": response}


def match_resume_to_jd(state: ChatState):
    jd_data = state['jd_data']
    resume_data = state['resume_data']
    model = getModel()
    
    structured_model = model.with_structured_output(MatchSchema)
    # Note: Pydantic models will be stringified properly by the prompt formatting
    prompt = MATCH_ANALYZER_PROMPT.format(resume_data=resume_data, jd_data=jd_data)

    response = structured_model.invoke(prompt)
    return {"match_data": response}


def tailor_resume(state: ChatState):
    resume = state['resume']
    resume_data = state['resume_data']
    jd_data = state['jd_data']
    match_data = state['match_data']
    evaluation_data = state.get('evaluated_data', '')
    
    prompt = TAILOR_RESUME_PROMPT.format(
        resume=resume, 
        resume_data=resume_data, 
        jd_data=jd_data, 
        match_data=match_data, 
        evaluation_data=evaluation_data
    )
    
    model = getModel()
    response = model.invoke(prompt)
    content = response.content
    
    # 1. Handle Gemini's list format
    if isinstance(content, list):
        content = "".join(
            block.get("text", "") for block in content if isinstance(block, dict) and "text" in block
        )
        
    # 2. Handle NVIDIA's JSON string format (e.g., { "resume": "..." })
    content = content.strip()
    if content.startswith("{") and "resume" in content[:50]:
        try:
            parsed = json.loads(content)
            if isinstance(parsed, dict) and "resume" in parsed:
                content = parsed["resume"]
        except Exception:
            # If JSON parsing fails (e.g., markdown fences around it), extract manually
            match = re.search(r'"resume"\s*:\s*"(.*)"', content, re.DOTALL)
            if match:
                content = match.group(1)
                
    # 3. Fix literal \n characters if they exist
    # (Sometimes models return "Line 1\\nLine 2" instead of actual newlines)
    if "\\n" in content:
        content = content.replace("\\n", "\n")

    return {'tailored_resume': content}


def evaluate_resume(state: ChatState):
    resume = state['resume']
    resume_data = state['resume_data']
    jd_data = state['jd_data']
    match_data = state['match_data']
    tailored_resume = state['tailored_resume']
    
    prompt = EVALUATION_PROMPT.format(
        resume=resume, 
        resume_data=resume_data, 
        jd_data=jd_data, 
        match_data=match_data, 
        tailored_resume=tailored_resume
    )

    model = getModel()
    structured_model = model.with_structured_output(EvaluatorSchema)
    
    response = structured_model.invoke(prompt)
    return {
        'evaluated_data': response, 
        'revision_count': state.get('revision_count', 0) + 1
    }


def revise_data(state: ChatState):
    if state['evaluated_data'].passed:
        return 'END'

    if state.get('revision_count', 0) >= 5:
        return 'END'
    return 'tailor_resume'