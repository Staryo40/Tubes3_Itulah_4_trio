
class TrieNode:
    def __init__(self, value=None):
        self.value = value
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self, keyword_array):
        self.root = TrieNode()
        self.create_trie(keyword_array)

    def create_trie(self, keyword_array):
        for word in keyword_array:
            if word:
                current_node = self.root
                for char in word.lower():
                    if char not in current_node.children:
                        new_node = TrieNode(char)
                        new_node.parent = current_node 
                        current_node.children[char] = new_node
                    current_node = current_node.children[char]
                current_node.is_end_of_word = True
    
    def print_trie(self):
        self.trie_dfs(self.root, "")
    
    def trie_dfs(self, node, prefix):
        for char, child in node.children.items():
            new_prefix = prefix + char
            print(new_prefix + (" [end]" if child.is_end_of_word else ""))
            self.trie_dfs(child, new_prefix)

if __name__ == "__main__":
    trie = Trie(["apple", "app", "apt", "bat", "batch"])
    trie.print_trie()
