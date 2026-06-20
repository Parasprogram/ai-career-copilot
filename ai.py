import os
import json
from openai import OpenAI

api_key = os.getenv(
    "OPENAI_API_KEY",
    "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"
)

client = OpenAI(api_key=api_key)

def analyze_resume(resume_text, user_goal):
    prompt=f"""
        you are a senior software engineer and hiring manager. Evaluate the resume based on the user's goal.
        
        user_goal: {user_goal}
        
        STRICT RULES:
        1. Extract only skills for this goal.
        2. Remove irrelevant tools [excel for backend etc].
        3. Identify the real gaps.
        4. Generate roadmap only for the missing fields.
        5. Make output DIFFERENT based on goal.
        
        Return only JSON:
        {{
            "Skills":[],
            "Missing Skills":[],
            "Roadmap":[]
            "Interview Questions":[]
        }}
        
        Resume:
        {resume_text}
    """
    
    try:
        response=client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system", "content":"You are a helpful assistant."},
                    {"role":"user", "content":prompt}
                ],
                temperature=0.7,
            )
            
        content=response.choices[0].message.content.strip()
        start=content.find("{")
        end=content.rfind("}")
        return json.loads(content[start:end])
    except Exception as e:
        return{
            "skills":[],
            "missing_skills":[],
            "roadmap":[],
            "interview_questions":[],
            "error":str(e)
        }