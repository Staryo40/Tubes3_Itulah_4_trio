import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """Extracts plain text from all pages of a PDF file."""
    doc = fitz.open(pdf_path)
    full_text = ""
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text") 
        full_text += text + "\n" 

    return full_text.strip()


def extract_from_pdf(pdf_path):
    """Extracts text from a PDF file, heuristically preserving bullet points."""
    doc = fitz.open(pdf_path)
    full_text = ""

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                line_text = ""
                spans = line["spans"]
                if not spans:
                    continue

                first_x = spans[0]["bbox"][0]
                text_parts = [span["text"].strip() for span in spans if span["text"].strip()]
                line_text = " ".join(text_parts).strip()

                # Heuristic: if indented (x > 50) but not far (x < 150), treat as list item
                if 50 < first_x < 200 and len(line_text.split()) < 30:
                    full_text += "- " + line_text + "\n"
                else:
                    full_text += line_text + "\n"
        full_text += "\n"

    return full_text.strip()

def inspect_bullet_spans(pdf_path):
    """Prints all span texts in the PDF for bullet detection debugging."""
    doc = fitz.open(pdf_path)

    for page_number, page in enumerate(doc):
        print(f"\n--- Page {page_number + 1} ---")
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line.get("spans", []):
                    print(repr(span["text"]))

# Example usage
if __name__ == "__main__":
    pdf_path = "test.pdf"  
    # text = extract_from_pdf(pdf_path)
    # print(text)
    # print(repr(text))

    inspect_bullet_spans(pdf_path)
