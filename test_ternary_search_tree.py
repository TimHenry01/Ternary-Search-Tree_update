import unittest
import sys
import os

# Add the parent directory to the path to import our module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ternary_search_tree import TernarySearchTree

# Test cases for TernarySearchTree class.
class TestTernarySearchTree(unittest.TestCase):
    
    # Set up test fixtures before each test method.
    def setUp(self):
        self.tst = TernarySearchTree()
        self.sample_words = ["cat", "cats", "up", "bug", "add", "at", "apple", "application"]
    
    # Test inserting a single word.
    def test_insert_single_word(self):
        self.tst.insert("hello")
        self.assertEqual(len(self.tst), 1)
        self.assertTrue(self.tst.search("hello", exact=True))
        self.assertIn("hello", self.tst.all_strings())
    
    # Test inserting multiple words.
    def test_insert_multiple_words(self):
        for word in self.sample_words:
            self.tst.insert(word)
        
        self.assertEqual(len(self.tst), len(self.sample_words))
        for word in self.sample_words:
            self.assertTrue(self.tst.search(word, exact=True))
    
    # Test that duplicate words are not inserted.
    def test_insert_duplicate_words(self):
        self.tst.insert("hello")
        self.tst.insert("hello")  # Duplicate
        
        self.assertEqual(len(self.tst), 1)
        self.assertTrue(self.tst.search("hello", exact=True))
    
    # Test searching for words that exist.
    def test_search_existing_words(self):
        for word in self.sample_words:
            self.tst.insert(word)
        
        for word in self.sample_words:
            self.assertTrue(self.tst.search(word, exact=True))
            
    # Test searching for prefixes.
    def test_search_for_prefixes(self):
        self.tst.insert("apple")
        self.tst.insert("application")
        self.assertTrue(self.tst.search("app"))
        self.assertTrue(self.tst.search("appl"))
        self.assertTrue(self.tst.search("applic"))
        self.assertFalse(self.tst.search("appli", exact=True)) # 'appli' is a prefix, not a full word
    
    # Test searching for words that don't exist.
    def test_search_non_existing_words(self):
        for word in self.sample_words:
            self.tst.insert(word)
        
        self.assertFalse(self.tst.search("nonexistent", exact=True))
        self.assertFalse(self.tst.search("catss", exact=True)) # Extension of "cats"
    
    # Test search with invalid input.
    def test_search_invalid_input(self):
        self.assertFalse(self.tst.search(""))
        self.assertFalse(self.tst.search(None))
        self.assertFalse(self.tst.search(123))
    
    # Test retrieving all strings from the tree.
    def test_all_strings(self):
        for word in self.sample_words:
            self.tst.insert(word)
        
        all_words = self.tst.all_strings()
        self.assertEqual(set(all_words), set(self.sample_words))
    
    # Test handling of case and whitespace in input.
    # Note: Your provided TST code did not include case or whitespace handling.
    # This test assumes you will add this functionality.
    def test_case_and_whitespace_handling(self):
        self.tst.insert("  Hello  ")
        self.tst.insert("WORLD")
        
        self.assertTrue(self.tst.search("hello", exact=True))
        self.assertTrue(self.tst.search("world", exact=True))
        self.assertTrue(self.tst.search("HELLO", exact=True))
        self.assertFalse(self.tst.search("  Hello  ", exact=True)) # Test with leading/trailing spaces
    
    # Test various edge cases.
    def test_edge_cases(self):
        # Single character words
        self.tst.insert("a")
        self.tst.insert("b")
        self.tst.insert("c")
        
        self.assertTrue(self.tst.search("a", exact=True))
        self.assertTrue(self.tst.search("b", exact=True))
        self.assertTrue(self.tst.search("c", exact=True))
        
        # Words with common prefixes
        prefixed_words = ["test", "testing", "tester", "tests"]
        for word in prefixed_words:
            self.tst.insert(word)
        
        for word in prefixed_words:
            self.assertTrue(self.tst.search(word, exact=True))
        
        # Test prefixes of these words
        self.assertTrue(self.tst.search("test")) # Prefix of 'test', 'testing', 'tester', 'tests'
        self.assertTrue(self.tst.search("testi")) # Prefix of 'testing'
        self.assertFalse(self.tst.search("test", exact=True)) # Exact match for 'test'
        self.assertFalse(self.tst.search("tester", exact=False))
