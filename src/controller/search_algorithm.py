from local_enum import *
from .aho_corasick import AhoCorasickSearch
import re


class SearchAlgorithm:
    def __init__(self, text, keyword):
        self.keyword = keyword
        self.text = text
        self.text_length = len(self.text)
        self.keyword_length = len(self.keyword)
    
    def exact_search_result(self, algo: MatchingAlgorithm):
        "returns exact matching using KMP or BM, output: (<number of matches>, <whole text with highlight for matches>)"
        indices = []
        start = 0

        while start < self.text_length:
            if (algo == MatchingAlgorithm.KMP):
                match_index = self.kmp_search(start)
            elif (algo == MatchingAlgorithm.BM):
                match_index = self.boyer_moore_search(start)

            if match_index == -1:
                break
            indices.append(match_index)
            start = match_index + self.keyword_length 

        if not indices:
            return (0, self.text)

        result = ""
        last_index = 0
        for index in indices:
            result += self.text[last_index:index]
            result += "\033[91m" + self.text[index:index+self.keyword_length] + "\033[0m"
            last_index = index + self.keyword_length

        result += self.text[last_index:]
        return (len(indices), result)
    
    def exact_search_indexes(self, algo: MatchingAlgorithm):
        "return starting indexes of exact matches"
        indices = []
        start = 0

        while start < self.text_length:
            if (algo == MatchingAlgorithm.KMP):
                match_index = self.kmp_search(start)
            elif (algo == MatchingAlgorithm.BM):
                match_index = self.boyer_moore_search(start)

            if match_index == -1:
                break
            indices.append(match_index)
            start = match_index + self.keyword_length 

        return indices
    
    def similar_search_result(self, threshold, method: LevenshteinMethod):
        "returns similar matching using levenshtein, output: (<number of matches>, <whole text with highlight for matches>)"
        result = ""
        last_index = 0
        start = 0
        found = 0

        while start <= self.text_length - self.keyword_length:
            if method == LevenshteinMethod.WORD:
                match_index = self.levenshtein_search_word(threshold, start)
            elif method == LevenshteinMethod.WINDOW:
                match_index = self.levenshtein_search_window(threshold, start)
            else:
                break

            if match_index == -1:
                break
            found += 1

            if method == LevenshteinMethod.WORD:
                word_match = re.match(r"[\w']+", self.text[match_index:])
                if not word_match:
                    break
                matched_text = word_match.group()
                match_end = match_index + len(matched_text)
            elif method == LevenshteinMethod.WINDOW:
                matched_text = self.text[match_index:match_index + self.keyword_length]
                match_end = match_index + self.keyword_length

            result += self.text[last_index:match_index]
            result += "\033[93m" + matched_text + "\033[0m" # yellow
            last_index = match_end

            if method == LevenshteinMethod.WORD:
                next_space = self.text.find(' ', match_end)
                start = next_space + 1 if next_space != -1 else self.text_length
            else:
                start = last_index

        result += self.text[last_index:]
        return (found, result)

    def similar_search_indexes(self, threshold, method: LevenshteinMethod):
        "return starting indexes of similar matches"
        last_index = 0
        start = 0
        indices = []

        while start <= self.text_length - self.keyword_length:
            if method == LevenshteinMethod.WORD:
                match_index = self.levenshtein_search_word(threshold, start)
            elif method == LevenshteinMethod.WINDOW:
                match_index = self.levenshtein_search_window(threshold, start)
            else:
                break

            if match_index == -1:
                break
            indices.append(match_index)

            if method == LevenshteinMethod.WORD:
                word_match = re.match(r"[\w']+", self.text[match_index:])
                if not word_match:
                    break
                matched_text = word_match.group()
                match_end = match_index + len(matched_text)
            elif method == LevenshteinMethod.WINDOW:
                matched_text = self.text[match_index:match_index + self.keyword_length]
                match_end = match_index + self.keyword_length

            last_index = match_end

            if method == LevenshteinMethod.WORD:
                next_space = self.text.find(' ', match_end)
                start = next_space + 1 if next_space != -1 else self.text_length
            else:
                start = last_index

        return indices
    
    def boyer_moore_search(self, search_start=0):
        """Return index where pattern starts in text using Boyer-Moore bad character rule, or -1 if no match."""
        last = self.build_last_occur()
        n = self.text_length
        m = self.keyword_length
        i = search_start + m - 1  

        if i >= n:
            return -1 

        j = m - 1

        while i < n:
            if self.keyword[j].lower() == self.text[i].lower():
                if j == 0:
                    return i  
                else:
                    i -= 1
                    j -= 1
            else:
                lo = last[self.text[i]] if self.text[i] in last else -1
                i += m - min(j, 1 + lo)
                j = m - 1

        return -1 
    
    def build_last_occur(self):
        """Return map storing of last occurrences of each ASCII char in pattern."""
        last = {}
        for i in range(self.keyword_length):
            last[self.keyword[i]] = i 
        return last

    def kmp_search(self, search_start=0):
        b = self.kmp_border_func()
        i = search_start
        j = 0
        while (i < self.text_length):
            if (self.text[i].lower() == self.keyword[j].lower()):
                if (j == self.keyword_length-1):
                    return i - self.keyword_length + 1
                i += 1
                j += 1
            elif (j > 0):
                j = b[j-1]
            else:
                i += 1
        return -1

    def kmp_border_func(self):
        b = [0] * self.keyword_length
        j = 0
        i = 1

        while (i < self.keyword_length):
            if (self.keyword[j] == self.keyword[i]):
                b[i] = j + 1
                i += 1
                j += 1
            elif (j > 0):
                j = b[j-1]
            else:
                b[i] = 0
                i += 1
        return b
    
    def levenshtein_search_window(self, threshold, search_start=0):
        """Return the first index at or after search_start where the pattern matches with Levenshtein distance <= threshold."""
        n = self.text_length
        m = self.keyword_length

        for i in range(search_start, n - m + 1):
            window = self.text[i:i + m]
            dist = self.levenshtein_distance(self.keyword.lower(), window.lower())
            if dist <= threshold:
                return i

        return -1
    
    def levenshtein_search_word(self, threshold, search_start=0):
        """Return the index in text where a word matches keyword within threshold. Search starts at char index `search_start`."""
        text = self.text[search_start:].lower()
        matches = list(re.finditer(r"[\w']+", text)) 

        for match in matches:
            word = match.group()
            # print(word)
            start_index = match.start() + search_start 
            dist = self.levenshtein_distance(self.keyword.lower(), word)
            if dist <= threshold:
                return start_index

        return -1

    def levenshtein_distance(self, a, b):
        # print(f"Comparing: '{a}' vs '{b}'")
        """Compute the Levenshtein distance between strings a and b."""
        sub_cost = 1
        del_cost = 1
        ins_cost = 1
        m, n = len(a), len(b)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                insertion = dp[i][j - 1] + ins_cost
                deletion = dp[i - 1][j] + del_cost
                substitution = dp[i - 1][j - 1] + (0 if a[i - 1] == b[j - 1] else sub_cost)
                dp[i][j] = min(insertion, deletion, substitution)
        
        # print("DP Matrix:")
        # for row in dp:
        #     print(row)
        # print(f"Distance = {dp[m][n]}")
        return dp[m][n]

class MultipleKeywordSearch:
    def __init__(self, text, keywords):
        self.text = text
        self.keywords = keywords
        self.n_key = len(keywords)
    
    def keywords_search_result(self, lev_threshold, lev_method: LevenshteinMethod, algo: MatchingAlgorithm):
        "Get matching results from each keyword, gets both exact and fuzzy results if exact is not found"
        result = {}
        if algo == MatchingAlgorithm.AC:
            aho = AhoCorasickSearch(self.text, self.keywords)
            aho_res = aho.ah_search_indexes()

            for key, indexes in aho_res.items():
                if len(indexes) == 0:
                    search = SearchAlgorithm(self.text, key)
                    fuzzy = search.similar_search_indexes(lev_threshold, lev_method)
                    if fuzzy:
                        result[key] = {
                            "type": KeywordResult.Similar,
                            "occurrence": len(fuzzy)
                        }
                    else:
                        result[key] = {
                            "type": KeywordResult.NotFound,
                            "occurrence": 0
                        }
                else:
                    result[key] =  { "type": KeywordResult.Exact,
                                    "occurrence": len(indexes) }
            print(result)
        else:
            for word in self.keywords:
                search = SearchAlgorithm(self.text, word)

                exact = search.exact_search_indexes(algo)
                if (exact and len(exact) > 0):
                    result[word] = { "type": KeywordResult.Exact,
                                    "occurrence": len(exact) }
                    continue
                
                fuzzy = search.similar_search_indexes(lev_threshold, lev_method)
                if (fuzzy and len(fuzzy) > 0):
                    result[word] = { "type": KeywordResult.Similar,
                                    "occurrence": len(fuzzy) }
                    continue
                
                if (len(fuzzy) <= 0 and len(exact) <= 0):
                    result[word] = { "type": KeywordResult.NotFound,
                                    "occurrence": 0 }
        
        return result

    def total_match_count(self, keyword_dic):
        exact = self.exact_match_count(keyword_dic)
        similar = self.similar_match_count(keyword_dic)
        return exact + similar
        
    def similar_match_count(self, keyword_dic):
        count = 0
        for word, content in keyword_dic.items():
            if content['type'] == KeywordResult.Similar:
                count += content['occurrence']
        return count
    
    def exact_match_count(self, keyword_dic):
        count = 0
        for word, content in keyword_dic.items():
            if content['type'] == KeywordResult.Exact:
                count += content['occurrence']
        return count

if __name__ == "__main__":
    new = SearchAlgorithm("", "ababababca")
    border = new.kmp_border_func()
    print(border)

    flower = SearchAlgorithm("Flowers, also known as blooms and blossoms, are the reproductive structures of flowering plants", "flower")
    print(flower.exact_search_result(MatchingAlgorithm.KMP)[1])
    print(flower.exact_search_result(MatchingAlgorithm.BM)[1])
    print(flower.similar_search_result(1, LevenshteinMethod.WORD)[1])