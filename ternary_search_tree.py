class TernarySearchTree:
    #Tree initialization 
    def __init__(self):
        self.root = None #Because there are no words yet
        self.word_count = 0 #Keeps track of how many words are inserted
        self.words_list = [] #Keeps track of all inserted words

    #Node initialization
    class Node:
        def __init__(self, char):
            self.char = char #Letter that is stored in the node
            self.end_of_word = False #True when the letter is the end of the word
            self._ls = None #Next node that has a character lesser
            self._eq = None #Next node that is the following character of the word
            self._gt = None #Nets node that has a character greater

    #Length of the tree
    def __len__(self):
        return self.word_count #returns number of words

    #Words inside the tree
    def all_strings(self):
        return self.words_list #returns list of words

    #Helper function for inserting words
    def insert_character(self, node, word, index):
        char = word[index] #character to insert

        if node is None:
            node = self.Node(char) #creates a new node if there is none already

        if char < node.char:
            node._ls = self.insert_character(node._ls, word, index) #go left
        elif char > node.char:
            node._gt = self.insert_character(node._gt, word, index) #go right
        else:
            if index + 1 == len(word):
                node.end_of_word = True #marks as end of the word
            else:
                node._eq = self.insert_character(node._eq, word, index + 1) #go middle

        return node

    #Insert word function
    def insert(self, word):
            
        if word not in self.words_list: #only for words not already inserted
            self.words_list.append(word)#updates list of all words
            self.word_count += 1 #updates the number of words added
            
        if word == '':
            return  # doesn't insert empty strings into the tree

        self.root = self.insert_character(self.root, word, 0)

    #Helper function for tree visualization
    def _str_helper(self, node, prefix="    ", child=""):
        child = f"{child}:" if child else "" #add the ":" for the childs
        lines = [f"{child} {prefix} char: {node.char}, terminates: {node.end_of_word}"] #structure of each line of the tree

        if node._ls:
            lines.append(self._str_helper(node._ls, prefix + "  ", "_ls")) #looping for left nodes
        if node._eq:
            lines.append(self._str_helper(node._eq, prefix + "  ", "_eq")) #looping for middle nodes
        if node._gt:
            lines.append(self._str_helper(node._gt, prefix + "  ", "_gt")) #looping for right nodes

        return "\n".join(lines) #combines all lines into one string

    #Tree visualization
    def __str__(self):
        if self.root is None:
            return "" #return nothing if tree is empty
        return "terminates: False\n" + self._str_helper(self.root) #starts visualization starting from the root


    #Helper function for search tool
    def search_helper(self, node, word, index):
        if node is None:
            return None #if the node doesn't exist, then the word doesn't either

        char = word[index] #current letter to compare
        
        if char < node.char:
            return self.search_helper(node._ls, word, index) #going to left node
        
        elif char > node.char:
            return self.search_helper(node._gt, word, index) #going to right node
        
        else:
            if index + 1 == len(word):
                return node #return node if last character
            return self.search_helper(node._eq, word, index + 1) #going to middle node

    #Search tool
    def search(self, word, exact=False):
        if word == '':
            return False #empty string are not stored in the tree

        node = self.search_helper(self.root, word, 0) #search for the node matching the last character
        
        if not node:
            return False #if the node doesn't exist, then the word doesn't either

        return True #word found

    def delete(self, word):
        """
        Delete a word from the ternary search tree.
        
        Args:
            word (str): The word to delete
            
        Returns:
            bool: True if word was deleted, False if word didn't exist
        """
        if not isinstance(word, str) or not word:
            return False
        
        word = word.lower().strip()
        if not word or not self._contains(word):
            return False
        
        self.root = self._delete_recursive(self.root, word, 0)
        self.word_count -= 1
        return True

    def _delete_recursive(self, node, word, index):
        """
        Recursively delete a word from the tree.
        
        Args:
            node: Current node
            word: Word being deleted
            index: Current character index
            
        Returns:
            Node: The root of the subtree after deletion
        """
        if node is None:
            return None
        
        char = word[index]
        
        if char < node.char:
            node._ls = self._delete_recursive(node._ls, word, index)
        elif char > node.char:
            node._gt = self._delete_recursive(node._gt, word, index)
        else:  # char == node.char
            if index == len(word) - 1:
                node.end_of_word = False
            else:
                node._eq = self._delete_recursive(node._eq, word, index + 1)
        
        # Remove node if it's not useful anymore
        if (not node.end_of_word and 
            node._ls is None and 
            node._eq is None and 
            node._gt is None):
            return None
        
        return node

    def is_empty(self):
        """
        Check if the tree is empty.
        
        Returns:
            bool: True if tree is empty, False otherwise
        """
        return self.root is None

    def clear(self):
        """Clear all words from the tree."""
        self.root = None
        self.word_count = 0

    def height(self):
        """
        Calculate the height of the tree.
        
        Returns:
            int: Height of the tree (0 for empty tree)
        """
        return self._height_recursive(self.root)

    def _height_recursive(self, node):
        """
        Recursively calculate height of subtree.
        
        Args:
            node: Root of subtree
            
        Returns:
            int: Height of subtree
        """
        if node is None:
            return 0
        
        left_height = self._height_recursive(node._ls)
        equal_height = self._height_recursive(node._eq) 
        right_height = self._height_recursive(node._gt)
        
        return 1 + max(left_height, equal_height, right_height)

    def __repr__(self):
        """Detailed string representation."""
        return f"TernarySearchTree(words={len(self)}, height={self.height()})"
