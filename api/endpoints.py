# pdf conversion endpoint
import os
from flask import json, jsonify, request
from flask_cors import cross_origin
import requests
import threading
from utils.gemini import generate
from google.generativeai.types.content_types import BlobDict


class GenerateFlashcardsEndpoint:
    def __init__(self, app):
        self.app = app

        @app.route('/generate', methods=['POST'])
        @cross_origin(origins="*")
        def generate_flashcards():
            # generation data
            data = request.form.get('data')
            data = json.loads(data)
            input_type = data['inputType']
            input_format = data['inputFormat']
            payment_type = data['paymentType']
            group_id = data['groupId']
            user_id = data['userId']
            # generation prompt
            text = request.form.get('text')
            course_info = request.form.get('courseInfo')
            image = request.files.get('image')
            if image:
                image = image.stream.read()
            pdf = request.files.get('pdf')
            if pdf:
                pdf = pdf.stream.read()
            pptx = request.files.get('pptx')
            if pptx:
                pptx = pptx.stream.read()

            if not text and not course_info and not pptx and not pdf and not image:
                return jsonify({"error": "Missing required fields"}), 400

            if not input_type or not input_format or not payment_type or not group_id or not user_id:
                return jsonify({"error": "Missing required fields"}), 400

            create_thread(self.generate_and_send_flashcards, group_id, user_id, input_type,
                          input_format, payment_type, text, image, pdf, pptx, course_info)
            return jsonify({"message": "Flashcards generation started"}), 200

    def format_gemini_input(self, text, image, pdf, pptx, course_info):
        file = None
        if pdf:
            file = BlobDict(data=pdf, mime_type="application/pdf")
        elif image:
            file = BlobDict(data=image, mime_type="image/jpeg")
        elif pptx:
            file = BlobDict(
                data=pptx, mime_type="application/vnd.openxmlformats-officedocument.presentationml.presentation")
        if course_info:
            text = course_info
        return text, file

    def generate_and_send_flashcards(self, group_id, user_id, input_type, input_format,
                                     payment_type, text, image, pdf, pptx, course_info):
        text, file = self.format_gemini_input(
            text, image, pdf, pptx, course_info)
        flashcards = generate(input_type, text, file,
                              is_free=payment_type == "free")
        body = {
            "flashcards": flashcards,
            "groupId": group_id,
            "userId": user_id,
            "inputType": input_type,
            "inputFormat": input_format,
            "paymentType": payment_type,
            "prompt": text if text else course_info if course_info else "Flashcards generated with a file",
        }
        requests.post(
            f"{os.environ['NODE_SERVER_URL']}/api/flashcards",
            json=body
        )


def create_thread(func, *args, **kwargs):
    thread = threading.Thread(target=func, args=args, kwargs=kwargs)
    thread.start()
    return thread
