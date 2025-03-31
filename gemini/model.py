import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from study_prompts import STUDY_PROMPTS
from write_prompts import WRITE_PROMPTS
from google.generativeai.types.content_types import BlobDict
import processing as process

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

def generate_flashcards(generate_type, text, file, is_free=False):
    prompts = {
        'notes': STUDY_PROMPTS['NOTES'],
        'syllabus': STUDY_PROMPTS['SYLLABUS'],
        'courseInfo': STUDY_PROMPTS['COURSE_INFO']
    }
    if generate_type not in prompts.keys():
        return {"error": "Invalid input type", "devError": f"Unrecognized input type: {generate_type}"}
    
    prompt = prompts.get(generate_type, {}).get('FREE' if is_free else 'PAID')
    return get_flashcard_output(prompt,text,file)


def generate_text(generate_type, text): 
    prompts = {
        'lengthen': WRITE_PROMPTS['LENGTHEN'],
        'shorten': WRITE_PROMPTS['SHORTEN'],
        'check_grammar': WRITE_PROMPTS['CHECK_GRAMMAR'],
        'auto_complete': WRITE_PROMPTS['AUTO_COMPLETE']
    }
    if generate_type not in prompts.keys():
        return {"error": "Invalid input type", "devError": f"Unrecognized input type: {generate_type}"}
    
    prompt=prompts.get(generate_type)
    return get_text_output(prompt, text, generate_type)


def get_text_output(prompt, text, generate_type):
    try:
        content = [prompt, text]
        response = model.generate_content(content)
        output = process.remove_text_formatting(response.text.strip())
        if generate_type != 'auto_complete':
            # print(output)
            process.check_similarity(text,output)
        return output
    except Exception as e:
        return {"error": "Failed to process request", "devError": str(e)}


def get_flashcard_output(prompt, text, file=None):
    try:
        content = [prompt, text if text else file]
        response = model.generate_content(content)
        output = process.remove_json_formatting(response.text.strip())
        json_output = json.loads(output)
        process.check_json(json_output)
        return json_output
    except Exception as e:
        return {"error": "Failed to generate flashcards", "devError": str(e)}


if __name__ == "__main__":

    data = json.dumps({
        'university': 'University of South Carolina',
        'department': 'Computer Science',
        'courseNumber': 'CSCE 581',
        'courseName': 'Trusted AI'
    })
    response = generate_flashcards("courseInfo", data, None, is_free=True)
    # response=generate_text("check_grammar",text)
    print(response)
