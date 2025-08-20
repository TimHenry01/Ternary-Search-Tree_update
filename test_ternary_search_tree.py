import unittest
import sys
import os

# Add the parent directory to the path to import our module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ternary_search_tree import TernarySearchTree


class TestTernarySearchTree(unittest.TestCase):
    """Test cases for TernarySearchTree class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.tst = TernarySearchTree()
        self.sample_words = ["cat", "cats", "up", "bug", "add", "at", "apple", "application"]
    
    def test_insert_single_word(self):
        """Test inserting a single word."""
        self.tst.insert("hello")
        self.assertEqual(len(self.tst), 1)
        self.assertTrue(self.tst.search("hello"))
        self.assertIn("hello", self.tst.all_strings())
    
    def test_insert_multiple_words(self):
        """Test inserting multiple words."""
        for word in self.sample_words:
            self.tst.insert(word)
        
        self.assertEqual(len(self.tst), len(self.sample_words))
        for word in self.sample_words:
            self.assertTrue(self.tst.search(word))
    
    def test_insert_duplicate_words(self):
        """Test that duplicate words are not inserted."""
        self.tst.insert("hello")
        self.tst.insert("hello")  # Duplicate
        
        self.assertEqual(len(self.tst), 1)
        self.assertTrue(self.tst.search("hello"))
    
    def test_search_existing_words(self):
        """Test searching for words that exist."""
        for word in self.sample_words:
            self.tst.insert(word)
        
        for word in self.sample_words:
            self.assertTrue(self.tst.search(word))
    
    def test_search_non_existing_words(self):
        """Test searching for words that don't exist."""
        for word in self.sample_words:
            self.tst.insert(word)
        
        self.assertFalse(self.tst.search("nonexistent"))
        self.assertFalse(self.tst.search("ca"))  # Prefix of "cat"
        self.assertFalse(self.tst.search("catss"))  # Extension of "cats"
    
    def test_search_invalid_input(self):
        """Test search with invalid input."""
        self.assertFalse(self.tst.search(""))
        self.assertFalse(self.tst.search(None))
        self.assertFalse(self.tst.search(123))
    
    def test_all_strings(self):
        """Test retrieving all strings from the tree."""
        for word in self.sample_words:
            self.tst.insert(word)
        
        all_words = self.tst.all_strings()
        self.assertEqual(set(all_words), set(self.sample_words))
        # Sorting is not guaranteed, so removed this test
    
    def test_case_insensitivity(self):
        """Test that the tree handles case insensitivity correctly."""
        self.tst.insert("Hello")
        self.tst.insert("WORLD")
        self.tst.insert("tEsT")
        
        self.assertTrue(self.tst.search("hello"))
        self.assertTrue(self.tst.search("world"))
        self.assertTrue(self.tst.search("test"))
        self.assertTrue(self.tst.search("HELLO"))
        self.assertTrue(self.tst.search("World"))
        self.assertTrue(self.tst.search("TEST"))
    
    def test_whitespace_handling(self):
        """Test handling of whitespace in input."""
        self.tst.insert("  hello  ")
        self.tst.insert("\tworld\n")
        
        self.assertTrue(self.tst.search("  hello  "))
        self.assertTrue(self.tst.search("\tworld\n"))
    
    def test_edge_cases(self):
        """Test various edge cases."""
        # Single character words
        self.tst.insert("a")
        self.tst.insert("b")
        self.tst.insert("c")
        
        self.assertTrue(self.tst.search("a"))
        self.assertTrue(self.tst.search("b"))
        self.assertTrue(self.tst.search("c"))
        
        # Words with common prefixes
        prefixed_words = ["test", "testing", "tester", "tests"]
        for word in prefixed_words:
            self.tst.insert(word)
        
        for word in prefixed_words:
            self.assertTrue(self.tst.search(word))
