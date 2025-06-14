from enum import Enum
import re

class matching_algorithm(Enum):
    KMP = 1
    BM = 2

class levenshtein_method(Enum):
    WORD = 1
    WINDOW = 2

class search_algorithm:
    def __init__(self, text, keyword):
        self.keyword = keyword
        self.text = text
        self.text_length = len(self.text)
        self.keyword_length = len(self.keyword)
    
    def exact_search_result(self, algo: matching_algorithm):
        indices = []
        start = 0

        while start < self.text_length:
            if (algo == matching_algorithm.KMP):
                match_index = self.kmp_search(start)
            elif (algo == matching_algorithm.BM):
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
    
    def similar_search_result(self, threshold, method: levenshtein_method):
        result = ""
        last_index = 0
        start = 0
        found = 0

        while start <= self.text_length - self.keyword_length:
            if method == levenshtein_method.WORD:
                match_index = self.levenshtein_search_word(threshold, start)
            elif method == levenshtein_method.WINDOW:
                match_index = self.levenshtein_search_window(threshold, start)
            else:
                break

            if match_index == -1:
                break
            found += 1

            if method == levenshtein_method.WORD:
                word_match = re.match(r"[\w']+", self.text[match_index:])
                if not word_match:
                    break
                matched_text = word_match.group()
                match_end = match_index + len(matched_text)
            elif method == levenshtein_method.WINDOW:
                matched_text = self.text[match_index:match_index + self.keyword_length]
                match_end = match_index + self.keyword_length

            result += self.text[last_index:match_index]
            result += "\033[93m" + matched_text + "\033[0m" # yellow
            last_index = match_end

            if method == levenshtein_method.WORD:
                next_space = self.text.find(' ', match_end)
                start = next_space + 1 if next_space != -1 else self.text_length
            else:
                start = last_index

        result += self.text[last_index:]
        return (found, result)

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
            if self.keyword[j] == self.text[i]:
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
            if (self.text[i] == self.keyword[j]):
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
            dist = self.levenshtein_distance(self.keyword, window)
            if dist <= threshold:
                return i

        return -1
    
    def levenshtein_search_word(self, threshold, search_start=0):
        """Return the index in text where a word matches keyword within threshold. Search starts at char index `search_start`."""
        text = self.text[search_start:]
        matches = list(re.finditer(r"[\w']+", text)) 

        for match in matches:
            word = match.group()
            # print(word)
            start_index = match.start() + search_start 
            dist = self.levenshtein_distance(self.keyword, word)
            if dist <= threshold:
                return start_index

        return -1

    def levenshtein_distance(self, a, b):
        # print(f"Comparing: '{a}' vs '{b}'")
        """Compute the Levenshtein distance between strings a and b."""
        sub_cost = 1
        del_cost = 0.5
        ins_cost = 0.5
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

new = search_algorithm("", "ababababca")
border = new.kmp_border_func()
print(border)

flower = search_algorithm("Flowers, also known as blooms and blossoms, are the reproductive structures of flowering plants", "ar")
print(flower.exact_search_result(matching_algorithm.KMP)[1])
print(flower.exact_search_result(matching_algorithm.BM)[1])
print(flower.similar_search_result(1, levenshtein_method.WORD)[1])