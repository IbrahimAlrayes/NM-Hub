import os
from dotenv import load_dotenv
load_dotenv()

LLM_CONFIGS ={
   'GEMINI_API_KEY' : os.getenv('GEMINI_API_KEY','')
}
