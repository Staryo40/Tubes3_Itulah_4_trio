from .pdf_text import *
from local_enum import *
import re
import json, os

header_dic = "data/header_dictionary.json"

class CVSummaryGenerator:
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
    
    def raw_summary_filter(self, summary_dic):
        filtered = {}
        for header, content in summary_dic.items():
            normalized = re.sub(r'\n{2,}', '\n', content.strip()) # get rid of extra new line
            normalized = re.sub(r'</list>\n<list>[a-z]', ' ', normalized.strip()) # combine long list element
            if '<list>' not in normalized and ',' in normalized: # make bullets
                items = [item.strip() for item in normalized.strip(", ").split(',') if item.strip()]
                word_counts = [len(item.split()) for item in items]
                if all(count <= 5 for count in word_counts):
                    normalized = '\n'.join(f"<bullet>{item}</bullet>" for item in items)
            filtered[header] = normalized

        return filtered     
    
    def final_summary_filter(self, summary_dic):
        filtered = {}
        for header, content in summary_dic.items():
            if '<bullet>' not in content:
                # filtered[header] = self.split_non_list_chunks(content)
                # filtered_arr = []
                # for text in filtered[header]:
                #     filtered_arr.append(re.sub(r'\n', ', ', text))
                filtered_arr = self.split_non_list_chunks(content)
                filtered[header] = {"type": TextFormat.List, "content": filtered_arr}
            else:
                bullet_arr = self.bullet_block_to_array(content)
                filtered[header] = {"type": TextFormat.List, "content": bullet_arr}
        return filtered

    def split_non_list_chunks(self, content):
        lines = content.strip().split('\n')

        if all(line.strip().startswith("<list>") and line.strip().endswith("</list>") for line in lines if line.strip()):
            return [re.sub(r"</?list>", "", line.strip()) for line in lines if line.strip()]
    
        result = []
        buffer = []

        for line in lines:
            line = line.strip()
            if line.startswith("<list>") and line.endswith("</list>"):
                # When we hit a <list>, treat it as a delimiter:
                if buffer:
                    joined = "\n".join(buffer).strip()
                    if joined:
                        result.append(joined)
                        buffer = []  # reset after chunk
                # Else: ignore list content entirely
            else:
                buffer.append(line)

        if buffer:
            joined = "\n".join(buffer).strip()
            if joined:
                result.append(joined)

        return result
    
    def bullet_block_to_array(self, bullet_block):
        return re.findall(r'<bullet>(.*?)</bullet>', bullet_block.strip(), re.DOTALL)
    
    def get_final_summary(self):
        summary = self.get_summary()
        raw_filtered = self.raw_summary_filter(summary)
        final_filtered = self.final_summary_filter(raw_filtered)

        return final_filtered

# pdf = pdf_extractor("test.pdf")
# text = pdf.pdf_pure_text()
# gen = cv_summary_generator(text)
# sum = gen.final_summary_filter(gen.raw_summary_filter(gen.get_summary()))
# for header, content in sum.items():
#     print(f"=== {header.upper()} ===")
#     print(content)
#     print("")
    
    