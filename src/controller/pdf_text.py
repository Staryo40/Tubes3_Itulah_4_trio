import fitz  # PyMuPDF
import re
import math

def extract_text_from_pdf(pdf_path):
    """Extracts plain text from all pages of a PDF file."""
    doc = fitz.open(pdf_path)
    full_text = ""
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text") 
        full_text += text

    return full_text.strip()

class PDFExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_raw_from_pdf(self):
        """Extracts raw text from all pages of a PDF file, replacing newlines with spaces."""
        doc = fitz.open(self.pdf_path)
        full_text = ""

        for page in doc:
            text = page.get_text("text")
            full_text += text

        cleaned_text = re.sub(r'[\n\r]+', ' ', full_text)
        
        return cleaned_text.strip()
    
    def extract_with_indent(self):
        doc = fitz.open(self.pdf_path)
        result = []

        for page in doc:
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                for line in block.get("lines", []):
                    spans = line.get("spans", [])
                    if not spans:
                        continue
                    x0 = spans[0]["bbox"][0]
                    text = " ".join(span["text"].strip() for span in spans).strip()
                    result.append((x0, text))

        return result

    def indent_text_to_format_text(self, ind_text_arr):
        min_x = math.inf
        for x, y in ind_text_arr:
            if (x < min_x):
                min_x = x
        
        result = ""
        for x, y in ind_text_arr:
            if (x > min_x):
                result += "<list>" + y + "</list>\n"
            else:
                result += y + "\n"
        
        return result

    def pdf_pure_text(self):
        ind = self.extract_with_indent()
        text = self.indent_text_to_format_text(ind)
        return text
    
# Example usage
if __name__ == "__main__":
    ext = PDFExtractor("test.pdf")
    print(ext.extract_raw_from_pdf())
