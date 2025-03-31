# pdf conversion endpoint
from flask import json, jsonify, request
from flask_cors import cross_origin
import requests
import threading
from utils.gemini import generate, gemini_improve_grammer
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

            text, file = self.format_gemini_input(
                text, image, pdf, pptx, course_info
            )

            flashcards = generate(input_type, text, file,
                                  is_free=payment_type == "free")

            return jsonify(flashcards), 200

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


class ImproveParagraphEndpoint:

    def __init__(self, app) -> None:
        self.app = app

        @app.route("/improve_paragraph", methods=["POST"])
        @cross_origin(origins="*")
        def imporve_paragraph():
            data = request.json
            context = data['context']
            target_paragraph = data['target_paragraph']
            operation_type = data['operation_type']

            # The if statements can change
            if (operation_type == "imporve_grammer"):
                improved_paragraph = gemini_improve_grammer(
                    context, target_paragraph)
                return jsonify(improved_paragraph), 200

            return jsonify({"error": ""}), 400
