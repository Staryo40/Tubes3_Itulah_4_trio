from collections import deque, defaultdict
from .trie import *

class AhoCorasickSearch:
    def __init__(self, text, keywords):
        self.text = text.lower()
        self.keywords = [kw.lower() for kw in keywords]
        self.trie = Trie(self.keywords)
        self.root = self.trie.root
        self._augment_nodes(self.root)
        self._build_failure_links()

    def _augment_nodes(self, node):
        """Recursively augment nodes with `fail` and `outputs`."""
        node.fail = None
        node.outputs = []
        if node.is_end_of_word:
            node.outputs.append(self._get_word_from_node(node))
        for child in node.children.values():
            self._augment_nodes(child)

    def _get_word_from_node(self, node):
        """Backtrack to reconstruct the keyword ending at this node."""
        chars = []
        while node and node.value:
            chars.append(node.value)
            node = node.parent
        return ''.join(reversed(chars))

    def _build_failure_links(self):
        queue = deque()
        for child in self.root.children.values():
            child.fail = self.root
            queue.append(child)
            child.parent = self.root  # manually set parent for path backtracking

        while queue:
            current_node = queue.popleft()
            for char, child in current_node.children.items():
                queue.append(child)
                fail_node = current_node.fail
                while fail_node and char not in fail_node.children:
                    fail_node = fail_node.fail
                child.fail = fail_node.children[char] if fail_node and char in fail_node.children else self.root
                child.outputs += child.fail.outputs
                child.parent = current_node  # set parent for reconstruction

    def ah_search_indexes(self):
        result = defaultdict(list)

        for keyword in self.keywords:
            result[keyword] = []

        node = self.root

        for i, char in enumerate(self.text):
            while node and char not in node.children:
                node = node.fail
            if not node:
                node = self.root
                continue
            node = node.children[char]
            for word in node.outputs:
                result[word].append(i - len(word) + 1)

        return dict(result)

if __name__ == "__main__":
    text = "bananas in bandana"
    keywords = ["ana", "ban", "in", "zzz"]

    search = AhoCorasickSearch(text, keywords)
    print(search.ah_search_indexes())
