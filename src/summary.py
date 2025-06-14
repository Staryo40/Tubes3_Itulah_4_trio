import re
import json
from pdf_text import extract_text_from_pdf

header_dic = "header_dictionary.json"

class cv_summary_generator:
    def __init__(self, text):
        self.text = text
    
    def read_header_dic(self):
        with open(header_dic, "r", encoding="utf-8") as file:
            header_dict = json.load(file)
            return header_dict

    def get_summary(self):
        header_map = {}
        all_headers = []
        for key, variants in self.read_header_dic().items():
            for variant in variants:
                norm = variant.lower()
                header_map[norm] = key
                all_headers.append(re.escape(norm))

        pattern = re.compile(rf"(?<=\n)({'|'.join(all_headers)})(?=\n)", re.IGNORECASE)

        normalized_text = "\n" + self.text.strip() + "\n"
        matches = list(pattern.finditer(normalized_text))

        result = {}
        for i, match in enumerate(matches):
            header_text = match.group(1).strip().lower()
            # header_key = header_map.get(header_text)
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(normalized_text)
            content = normalized_text[start:end].strip()
            result[header_text] = content

        return result
    
text = extract_text_from_pdf("test.pdf")
gen = cv_summary_generator(text)
sum = gen.get_summary()
for header, content in sum.items():
    lines = [line.strip() for line in content.strip().split("\n") if line.strip()]
    comma_items = [item.strip() for item in content.split(",") if item.strip()]

    # Case 1: content is likely a flat comma-separated list
    if len(comma_items) >= 5 and len(lines) == 1:
        print(f"=== {header.upper()} ===")
        for item in comma_items:
            print(f"- {item}")
        print("\n")

    # Case 2: content is a multi-line list (each line is a separate item)
    elif len(lines) >= 3 and all(len(line) < 120 for line in lines):
        print(f"=== {header.upper()} ===")
        for item in lines:
            print(f"- {item}")
        print("\n")

    # Otherwise, print normally as a paragraph
    else:
        print(f"=== {header.upper()} ===")
        print(content)
        print("\n")
    
    