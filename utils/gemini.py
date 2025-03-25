import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from utils.prompts import PROMPTS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="gemini-2.0-flash")


def generate(generate_type: str, text: str, is_free: bool = False):
    if not text:
        return {"error": "No provided input text"}

    if generate_type == 'notes':
        return generate_flashcards_from_notes(text, is_free)
    elif generate_type == 'syllabus':
        return generate_flashcards_from_syllabus(text, is_free)
    elif generate_type == 'courseInfo':
        try:
            course_info = json.loads(text)
            return generate_flashcards_from_course_info(
                course_info["university"],
                course_info["department"],
                course_info["courseNumber"],
                course_info["courseName"],
                is_free
            )
        except json.JSONDecodeError as e:
            return {"error": "Invalid input format", "devError": str(e)}
    else:
        return {"error": "Invalid input type", "devError": f"Unrecognized input type: {generate_type}"}


def generate_flashcards_from_syllabus(syllabus: str, is_free: bool):
    return get_output(PROMPTS['SYLLABUS']['FREE' if is_free else 'PAID'](syllabus))


def generate_flashcards_from_notes(notes: str, is_free: bool):
    return get_output(PROMPTS['NOTES']['FREE' if is_free else 'PAID'](notes))


def generate_flashcards_from_course_info(university: str, department: str, course_number: str, course_name: str, is_free: bool):
    return get_output(PROMPTS['COURSE_INFO']['FREE' if is_free else 'PAID'](university, department, course_number, course_name))


def get_output(prompt: str):
    try:
        response = model.generate_content(prompt)
        output = remove_formatting(response.text.strip())
        json_output = json.loads(output)
        check_json(json_output)
        return json_output
    except Exception as e:
        return {"error": "Failed to generate flashcards", "devError": str(e)}


def remove_formatting(text: str):
    # Remove ```json and ```
    if text.startswith("```json"):
        text = text[7:]
    if text.endswith("```"):
        text = text[:-3]
    return text


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
