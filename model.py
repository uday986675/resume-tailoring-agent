from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from gemini_coax import GeminiSafe
from dotenv import load_dotenv

load_dotenv()

def getModel():
    llm = ChatNVIDIA(
        model="nvidia/nemotron-3-ultra-550b-a55b",
        temperature=0.2,
        max_completion_tokens=4000,
        model_kwargs={
            "chat_template_kwargs": {
                "enable_thinking": False,
            },
            "response_format": {
                "type": "json_object",
            },
        },
    )

    # llm = GeminiSafe(
    #     model='gemini-3.8-flash',
    #     temperature=0       # Keeps JSON generation strictly formatted
    # )
    return llm