from enum import Enum

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
            return self.text

        result = ""
        last_index = 0
        for index in indices:
            result += self.text[last_index:index]
            result += "\033[91m" + self.text[index:index+self.keyword_length] + "\033[0m"
            last_index = index + self.keyword_length

        result += self.text[last_index:]
        return result
    
    def similar_search_result(self, threshold, method: levenshtein_method):
        """Highlight all approximate matches (within threshold) using Levenshtein distance in orange."""
        result = ""
        last_index = 0
        start = 0

        while start <= self.text_length - self.keyword_length:
            if (method == levenshtein_method.WORD):
                match_index = self.levenshtein_search_word(threshold, start)
            elif (method == levenshtein_method.WINDOW):
                match_index = self.levenshtein_search_window(threshold, start)
            if match_index == -1:
                break

            # Add text before the match
            result += self.text[last_index:match_index]

            # Highlight matched window in orange (color code: \033[93m)
            match_text = self.text[match_index:match_index + self.keyword_length]
            result += "\033[93m" + match_text + "\033[0m"

            # Update indices
            last_index = match_index + self.keyword_length
            start = last_index

        # Add any remaining text
        result += self.text[last_index:]
        return result

    def boyer_moore_search(self, search_start=0):
        """Return index where pattern starts in text using Boyer-Moore bad character rule, or -1 if no match."""
        last = self.build_last()
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
                lo = last[ord(self.text[i])] if ord(self.text[i]) < 128 else -1
                i += m - min(j, 1 + lo)
                j = m - 1

        return -1 
    
    def build_last(self):
        """Return array storing index of last occurrence of each ASCII char in pattern."""
        last = [-1] * 128  
        for i in range(self.keyword_length):
            last[ord(self.keyword[i])] = i
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
        """Return the index in text where a space-separated word matches keyword within threshold."""
        text = self.text[search_start:]
        words = text.split(" ")
        index = search_start

        for word in words:
            # Skip over leading/trailing spaces
            if not word:
                index += 1
                continue

            dist = self.levenshtein_distance(self.keyword, word)
            if dist <= threshold:
                return index

            index += len(word) + 1 

        return -1

    def levenshtein_distance(self, a, b):
        """Compute the Levenshtein distance between strings a and b."""
        m, n = len(a), len(b)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                cost = 0 if a[i - 1] == b[j - 1] else 1
                dp[i][j] = min(
                    dp[i - 1][j] + 1,    
                    dp[i][j - 1] + 1,   
                    dp[i - 1][j - 1] + cost 
                )

        return dp[m][n]

new = search_algorithm("", "ababababca")
border = new.kmp_border_func()
print(border)

flower = search_algorithm("Flowers, also known as blooms and blossoms, are the reproductive structures of flowering plants", "art")
print(flower.exact_search_result(matching_algorithm.KMP))
print(flower.exact_search_result(matching_algorithm.BM))
print(flower.similar_search_result(2, levenshtein_method.WORD))