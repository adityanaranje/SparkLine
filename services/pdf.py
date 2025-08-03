from xhtml2pdf import pisa
import markdown

class Pdffile:
    def save_markdown_as_pdf(self, text: str, file_path: str):
        html_body = markdown.markdown(text, extensions=["fenced_code", "codehilite"])

        html_template = f"""
        <html>
        <head>
        <style>
            body {{
                font-family: Helvetica, Arial, sans-serif;
                padding: 20px;
                font-size: 12pt;
            }}
            pre {{
                background-color: #f4f4f4;
                padding: 10px;
                border-radius: 5px;
                overflow-x: auto;
            }}
            code {{
                font-family: monospace;
                color: #333;
            }}
        </style>
        </head>
        <body>
            {html_body}
        </body>
        </html>
        """

        with open(file_path, "w+b") as f:
            pisa_status = pisa.CreatePDF(html_template, dest=f)

        if pisa_status.err: # type: ignore
            raise Exception("❌ Error generating PDF")
