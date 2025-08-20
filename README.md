# Ternary-Search-Tree
Ternary Search Tree Implementation
Course: Concepts of Data Science 2024-2025
Team Members: Maxwell Nuamah Appiah & Tim Henry
Repository: https://github.com/TimHenry01
Project Overview
This project implements a comprehensive Ternary Search Tree (TST) data structure in Python. A ternary search tree is a tree data structure that combines the time efficiency of digital tries with the space efficiency of binary search trees, making it particularly well-suited for string processing applications.
Features
Core Functionality
•	Insert: Add words to the tree with O(log n) average time complexity
•	Search: Find words in the tree with O(log n) average time complexity
•	Case Insensitive: Handles mixed case input automatically
•	Input Validation: Robust error handling for edge cases
Advanced Features
•	Memory Efficient: Optimized storage without redundant word lists
•	Comprehensive API: Full set of utility methods for tree management
•	Performance Monitoring: Built-in benchmarking capabilities
File Structure
project/
├── ternary_search_tree.py          # Main TST implementation
├── test_ternary_search_tree.py     # Comprehensive unit tests
├── benchmark_tst.py                # Performance benchmarking suite
├── ternary_search_tree.ipynb       # Jupyter notebook demonstration
├── hpc_job_script.slurm            # HPC job submission script
├── tst_performance_report.txt      # Performance report outpu
├── tst_performance_analysis.txt    # Performance graphs
├── Result analysis script          
├── job monitoring script 
└── README.md                       # This file

Installation and Setup
1.	Clone the repository:
2.	git clone [repository-url]
3.	cd ternary-search-tree
4.	Install dependencies:
5.	pip install -r requirements.txt
6.	Run tests to verify installation:
7.	python test_ternary_search_tree.py
Usage Examples
Basic Operations
from ternary_search_tree import TernarySearchTree

# Create a new TST
tst = TernarySearchTree()

# Insert words
tst.insert("cat")
tst.insert("cats")
tst.insert("dog")

# Search for words
print(tst.search("cat"))    # True
print(tst.search("car"))    # False

# Get all words
print(tst.all_strings())  # ['cat', 'cats', 'dog']
Advanced Usage

Testing
Our implementation includes comprehensive test coverage:
Running Tests
# Run all unit tests
python test_ternary_search_tree.py

# Run with verbose output
python test_ternary_search_tree.py -v
Test Coverage
•	Basic Operations: Insert, search
•	Edge Cases: Empty inputs, duplicates, case sensitivity
•	Error Handling: Invalid input types and edge conditions
•	Performance: Basic performance characteristics
•	Integration: Real-world usage scenarios
Performance Analysis
Benchmarking
Run comprehensive performance benchmarks:
# Quick benchmark (for testing)
python benchmark_tst.py --quick

# Full benchmark suite (takes longer)
python benchmark_tst.py
HPC Execution
For large-scale performance testing on HPC infrastructure:
# Submit job to HPC queue
sbatch hpc_job_script.sh

# Monitor job status
squeue -u $USER

# Check results
cat tst_benchmark_[JOB_ID].out
Performance Characteristics
Operation	Best Case	Average Case	Worst Case
Insert	O(log n)	O(log n)	O(n)
Search	O(log n)	O(log n)	O(n)
Delete	O(log n)	O(log n)	O(n)
Prefix	O(log n + k)	O(log n + k)	O(n + k)
Where n = number of words, k = number of results
Complexity Analysis
Time Complexity
•	Best/Average Case: O(log n) for most operations due to balanced tree structure
•	Worst Case: O(n) when tree becomes heavily unbalanced (e.g., sequential insertions)
