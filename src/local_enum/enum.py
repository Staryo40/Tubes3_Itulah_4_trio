from enum import Enum

class TextFormat(Enum):
    List = 1
    Bullet = 2

class MatchingAlgorithm(Enum):
    KMP = 1
    BM = 2
    AC = 3

class LevenshteinMethod(Enum):
    WORD = 1
    WINDOW = 2

class KeywordResult(Enum):
    Exact = 1
    Similar = 2
    NotFound = 3