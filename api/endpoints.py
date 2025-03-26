# pdf conversion endpoint
import os
from flask import jsonify, request
from flask_cors import cross_origin
import requests
import threading
from utils.pdf_extractor import PdfParser
from utils.pptx_extractor import get_text_from_pptx
from utils.gemini import generate


class PdfConversionEndpoint:
    def __init__(self, app):
        self.app = app

        @app.route('/pdf', methods=['POST'])
        @cross_origin(origins="*")
        def pdf_conversion():
            pdf_file = request.files["pdf"]
            pdf_binary_data = pdf_file.stream.read()
            extracted_text = ""
            try:
                parser = PdfParser(pdf_binary_data)
                extracted_text = parser.get_all_text_without_chapters()
                return jsonify(extracted_text)
            except Exception as e:
                return jsonify({"error": "Failed to process PDF file", "devError": str(e)}), 500


class PptxConversionEndpoint:
    def __init__(self, app):
        self.app = app

        @app.route('/pptx', methods=['POST'])
        @cross_origin(origins="*")
        def pptx_conversion():
            pptx_file = request.files['pptx']
            pptx_binary_data = pptx_file.stream.read()
            extracted_text = ""
            try:
                extracted_text = get_text_from_pptx(pptx_binary_data)
                return jsonify(extracted_text)
            except Exception as e:
                return jsonify({"error": "Failed to process PPTX file", "devError": str(e)}), 500


class GenerateFlashcardsEndpoint:
    def __init__(self, app):
        self.app = app

        @app.route('/generate', methods=['POST'])
        @cross_origin(origins="*")
        def generate_flashcards():
            data = request.json
            text = data['text']
            input_type = data['inputType']
            input_format = data['inputFormat']
            payment_type = data['paymentType']
            group_id = data['groupId']
            user_id = data['userId']

            if not text or not input_type or not input_format or not payment_type or not group_id or not user_id:
                return jsonify({"error": "Missing required fields"}), 400

            create_thread(self.generate_and_send_flashcards, group_id,
                          user_id, input_type, input_format, payment_type, text)
            return jsonify({"message": "Flashcards generation started"}), 200

    def generate_and_send_flashcards(self, group_id, user_id, input_type, input_format, payment_type, text):
        flashcards = generate(input_type, text, is_free=payment_type == "free")
        body = {
            "flashcards": flashcards,
            "groupId": group_id,
            "userId": user_id,
            "inputType": input_type,
            "inputFormat": input_format,
            "paymentType": payment_type,
            "prompt": text,
        }
        requests.post(
            f"{os.environ['NODE_SERVER_URL']}/api/flashcards",
            json=body
        )


def create_thread(func, *args, **kwargs):
    thread = threading.Thread(target=func, args=args, kwargs=kwargs)
    thread.start()
    return thread
