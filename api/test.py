from html2docx import html2docx

html = """
<h1>Hello World</h1>
<p>This is a <strong>test</strong> HTML content.</p>
"""
wrapped_html = f"""
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{
                        font-family: "Arial", sans-serif;
                        font-size: 14px;
                        line-height: 1.6;
                        padding: 40px;
                    }}
                    code {{
                        background-color: #f5f5f5;
                        padding: 2px 4px;
                        font-size: 90%;
                        border-radius: 4px;
                        font-family: monospace;
                    }}
                    pre {{
                        background-color: #f5f5f5;
                        padding: 12px;
                        border-radius: 6px;
                        font-family: monospace;
                        white-space: pre-wrap;
                    }}
                    .ProseMirror {{
                        max-width: 700px;
                        margin: auto;
                    }}
                </style>
            </head>
            <body>
                <div class="ProseMirror">{html}</div>
            </body>
            </html>
            """
# Convert HTML to a BytesIO object containing the .docx data
docx_bytes = html2docx(wrapped_html, title="Test Document")

# Write the BytesIO content to a .docx file
with open("output.docx", "wb") as f:
    f.write(docx_bytes.getvalue())
