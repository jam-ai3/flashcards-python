from pdf2image import convert_from_bytes



def convert_pdf_to_images(pdf_bytes):
    try:
        images = convert_from_bytes(pdf_bytes)
        return images
    except Exception as e:
        return {"error": "Cannot convert PDF to images", "devError": str(e)}
