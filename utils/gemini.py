import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from utils.prompts import PROMPTS
from utils.write_prompts import WRITE_PROMPTS
from google.generativeai.types.content_types import BlobDict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="gemini-2.0-flash")


def gemini_improve_grammer(context, target_paragraph):
    # Implement the prompt 
    return get_output_for_improve_grammer(WRITE_PROMPTS['IMPROVE_GRAMMER'](context, target_paragraph))



def generate(generate_type, text, file, is_free=False):
    if not text and not file:
        return {"error": "No text or file provided"}
    if generate_type == 'notes':
        return get_output(PROMPTS['NOTES']['FREE' if is_free else 'PAID'], text, file)
    elif generate_type == 'syllabus':
        return get_output(PROMPTS['SYLLABUS']['FREE' if is_free else 'PAID'], text, file)
    elif generate_type == 'courseInfo':
        return get_output(PROMPTS['COURSE_INFO']['FREE' if is_free else 'PAID'], text, file)
    else:
        return {"error": "Invalid input type", "devError": f"Unrecognized input type: {generate_type}"}


def get_output(prompt, text, file=None):
    try:
        content = [prompt, text if text else file]
        response = model.generate_content(content)
        output = remove_formatting(response.text.strip())
        json_output = json.loads(output)
        check_json(json_output)
        return json_output
    except Exception as e:
        return {"error": "Failed to generate flashcards", "devError": str(e)}


def get_output_for_improve_grammer(prompt):
    try:
        response = model.generate_content(prompt)
        output = remove_formatting(response.text.strip())
        json_output = json.loads(output)
        # The output should be only one item
        check_json_for_improve_grammer(json_output)
        output = json_output[0]['improved']
        return output
    except Exception as e:
        return {"error": "Failed to improve grammer", "devError": str(e)}

def remove_formatting(text):
    # Remove ```json and ```
    if text.startswith("```json"):
        text = text[7:]
    if text.endswith("```"):
        text = text[:-3]
    return text


def check_json_for_improve_grammer(text):
    for item in text:
        if not (isinstance(item, dict) and set(item.keys()) == {'improved'}):
            raise ValueError('Invalid JSON format')


def check_json(text):
    for item in text:
        if not (isinstance(item, dict) and set(item.keys()) == {'front', 'back'}):
            raise ValueError('Invalid JSON format')


if __name__ == "__main__":
    # Test
    data = json.dumps({
        'university': 'USC',
        'department': 'CSCE',
        'courseNumber': 581,
        'courseName': 'Trusted AI'
    })
    response = generate("course_info", data, is_free=True)
    print(response)
