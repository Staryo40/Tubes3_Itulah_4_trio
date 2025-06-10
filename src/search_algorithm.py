from enum import Enum

class matching_algorithm(Enum):
    KMP = 1
    BM = 2


class search_algorithm:
    def __init__(self, text, keyword):
        self.keyword = keyword
        self.text = text
        self.text_length = len(self.text)
        self.keyword_length = len(self.keyword)
    
    def get_search_result(self, algo):
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

new = search_algorithm("", "ababababca")
border = new.kmp_border_func()
print(border)

flower = search_algorithm("Flowers, also known as blooms and blossoms, are the reproductive structures of flowering plants", "plants")
print(flower.get_search_result(matching_algorithm.KMP))
print(flower.get_search_result(matching_algorithm.BM))