import time
import random
import string
import sys
import os
import gc
import tracemalloc
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import json

# Add the parent directory to the path to import our module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ternary_search_tree import TernarySearchTree

# Comprehensive benchmarking suite for Ternary Search Tree.
class TSTBenchmark:
    
    def __init__(self):
        self.results = defaultdict(dict)
        
    # Load words from a specified file path.
    def load_words_from_file(self, file_path, num_words=None):
        with open(file_path, 'r', encoding='utf-8') as f:
            words = [line.strip() for line in f if line.strip()]
        if num_words and num_words < len(words):
            return words[:num_words]
        return words
    
    # Generate random words for testing.
    def generate_random_words(self, count, min_length=3, max_length=10):
        words = []
        for _ in range(count):
            length = random.randint(min_length, max_length)
            word = ''.join(random.choices(string.ascii_lowercase, k=length))
            words.append(word)
        return list(set(words))  # Remove duplicates
    
    # Generate sequential words (worst case for some operations).
    def generate_sequential_words(self, count):
        return [f"word{i:06d}" for i in range(count)]
    
    # Generate words with similar prefixes (specific case analysis).
    def generate_similar_words(self, count, base="test"):
        words = [base]
        for i in range(1, count):
            suffix = ''.join(random.choices(string.ascii_lowercase, k=random.randint(1, 5)))
            words.append(f"{base}{suffix}")
        return words
    
    # Benchmark insert operation performance scaling.
    def benchmark_insert_performance(self, words, benchmark_name="Insert"):
        print(f"Benchmarking {benchmark_name} performance...")
        
        insert_times = []
        memory_usage = []
        word_counts = []

        tst = TernarySearchTree()

        tracemalloc.start()
        gc.collect()
        
        for i, word in enumerate(words):
            start_time = time.perf_counter()
            tst.insert(word)
            end_time = time.perf_counter()
            insert_times.append(end_time - start_time)
            word_counts.append(len(tst))
            
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        memory_usage.append(peak / 1024 / 1024)  # Convert to MB
        
        self.results[benchmark_name]['counts'] = word_counts
        self.results[benchmark_name]['times'] = insert_times
        self.results[benchmark_name]['memory'] = memory_usage
        
        print(f"  Total time for {len(words)} words: {sum(insert_times):.4f}s")
        print(f"  Peak memory usage: {memory_usage[0]:.2f}MB")
        
    # Benchmark search operation performance scaling.
    def benchmark_search_performance(self, words, benchmark_name="Search"):
        print(f"Benchmarking {benchmark_name} performance...")
        
        # First, insert all words to create the tree
        tst = TernarySearchTree()
        for word in words:
            tst.insert(word)
        
        search_times = []
        word_counts = []
        
        # Measure search time for each word
        for i, word in enumerate(words):
            start_time = time.perf_counter()
            tst.search(word)
            end_time = time.perf_counter()
            search_times.append(end_time - start_time)
            word_counts.append(i + 1)
            
        self.results[benchmark_name]['counts'] = word_counts
        self.results[benchmark_name]['times'] = search_times
        
        print(f"  Total time for {len(words)} searches: {sum(search_times):.4f}s")
    
    # Test worst-case scenarios for TST operations.
    def benchmark_worst_case_scenarios(self):
        print("Benchmarking worst-case scenarios...")
        
        scenarios = {
            'sequential_worst_case': self.generate_sequential_words(1000),
            'similar_prefixes_worst_case': self.generate_similar_words(1000, "commonprefix"),
        }
        
        for scenario_name, words in scenarios.items():
            print(f"  Testing {scenario_name} scenario...")
            
            tst = TernarySearchTree()
            
            # Measure insertion time
            start_time = time.perf_counter()
            for word in words:
                tst.insert(word)
            insert_time = time.perf_counter() - start_time
            
            # Measure search time
            start_time = time.perf_counter()
            for word in words:
                tst.search(word)
            search_time = time.perf_counter() - start_time
            
            # Store results
            self.results['worst_case'][scenario_name] = {
                'insert_time': insert_time,
                'search_time': search_time
            }
            
            print(f"    Insert: {insert_time:.4f}s, Search: {search_time:.4f}s")
    
    # Compare TST performance with Python's built-in data structures.
    def compare_with_builtin_structures(self, word_count=5000):
        print(f"Comparing with built-in structures ({word_count} words)...")
        
        words = self.generate_random_words(word_count)
        
        # Test TST
        tst = TernarySearchTree()
        start_time = time.perf_counter()
        for word in words:
            tst.insert(word)
        tst_insert_time = time.perf_counter() - start_time
        
        start_time = time.perf_counter()
        for word in words:
            tst.search(word)
        tst_search_time = time.perf_counter() - start_time
        
        # Test Python set
        python_set = set()
        start_time = time.perf_counter()
        for word in words:
            python_set.add(word)
        set_insert_time = time.perf_counter() - start_time
        
        start_time = time.perf_counter()
        for word in words:
            word in python_set
        set_search_time = time.perf_counter() - start_time
        
        # Test Python list (worst case)
        python_list = []
        start_time = time.perf_counter()
        for word in words:
            if word not in python_list:
                python_list.append(word)
        list_insert_time = time.perf_counter() - start_time
        
        start_time = time.perf_counter()
        for word in python_list:
            word in python_list
        list_search_time = time.perf_counter() - start_time
        
        # Store comparison results
        self.results['comparison'] = {
            'tst_insert': tst_insert_time,
            'tst_search': tst_search_time,
            'set_insert': set_insert_time,
            'set_search': set_search_time,
            'list_insert': list_insert_time,
            'list_search': list_search_time
        }
        
        print(f"  TST    - Insert: {tst_insert_time:.4f}s, Search: {tst_search_time:.4f}s")
        print(f"  Set    - Insert: {set_insert_time:.4f}s, Search: {set_search_time:.4f}s")
        print(f"  List   - Insert: {list_insert_time:.4f}s, Search: {list_search_time:.4f}s")
    
    def create_performance_plots(self):
        print("Creating performance plots...")
        
        # Create subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Insert performance plot
        if 'insert' in self.results and self.results['insert']:
            ax1.plot(self.results['insert']['counts'], self.results['insert']['times'], 'bo-', label='Insert Time')
            ax1.set_xlabel('Number of Words')
            ax1.set_ylabel('Time (seconds)')
            ax1.set_title('Insert Performance Scaling')
            ax1.grid(True)
            ax1.legend()
        
        # Search performance plot
        if 'search' in self.results and self.results['search']:
            ax2.plot(self.results['search']['counts'], self.results['search']['times'], 'ro-', label='Search Time')
            ax2.set_xlabel('Number of Words')
            ax2.set_ylabel('Time (seconds)')
            ax2.set_title('Search Performance Scaling')
            ax2.grid(True)
            ax2.legend()
        
        # Memory usage plot
        if 'insert' in self.results and self.results['insert']:
            ax3.plot(self.results['insert']['counts'], self.results['insert']['memory'], 'go-', label='Memory Usage')
            ax3.set_xlabel('Number of Words')
            ax3.set_ylabel('Memory (MB)')
            ax3.set_title('Memory Usage Scaling')
            ax3.grid(True)
            ax3.legend()
        
        # Comparison plot
        if 'comparison' in self.results:
            comp = self.results['comparison']
            structures = ['TST', 'Set', 'List']
            insert_times = [comp['tst_insert'], comp['set_insert'], comp['list_insert']]
            search_times = [comp['tst_search'], comp['set_search'], comp['list_search']]
            
            x = np.arange(len(structures))
            width = 0.35
            
            ax4.bar(x - width/2, insert_times, width, label='Insert', alpha=0.8)
            ax4.bar(x + width/2, search_times, width, label='Search', alpha=0.8)
            ax4.set_ylabel('Time (seconds)')
            ax4.set_title('Performance Comparison')
            ax4.set_xticks(x)
            ax4.set_xticklabels(structures)
            ax4.legend()
            ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('tst_performance_analysis.png', dpi=300, bbox_inches='tight')
        print("  Saved performance plots to 'tst_performance_analysis.png'")
    
    # Generate a comprehensive performance report.
    def generate_report(self):
        print("\nGenerating performance report...")
        
        report = []
        report.append("=" * 60)
        report.append("TERNARY SEARCH TREE PERFORMANCE ANALYSIS REPORT")
        report.append("=" * 60)
        report.append("")
        
        # Insert performance analysis
        if 'insert' in self.results and self.results['insert']:
            report.append("INSERT PERFORMANCE:")
            report.append("-" * 20)
            if 'counts' in self.results['insert'] and 'times' in self.results['insert']:
                for i, (count, time_taken) in enumerate(zip(self.results['insert']['counts'], self.results['insert']['times'])):
                    # Only show the final aggregate time for insert to avoid a huge report
                    if i == len(self.results['insert']['counts']) - 1:
                        report.append(f"  Total time for {count} words: {time_taken:.4f}s")
            report.append("")
        
        # Search performance analysis
        if 'search' in self.results and self.results['search']:
            report.append("SEARCH PERFORMANCE:")
            report.append("-" * 19)
            if 'counts' in self.results['search'] and 'times' in self.results['search']:
                for i, (count, time_taken) in enumerate(zip(self.results['search']['counts'], self.results['search']['times'])):
                    # Only show the final aggregate time for search
                    if i == len(self.results['search']['counts']) - 1:
                        report.append(f"  Total time for {count} searches: {time_taken:.4f}s")
            report.append("")
        
        # Worst case scenarios
        if 'worst_case' in self.results and self.results['worst_case']:
            report.append("WORST CASE SCENARIOS:")
            report.append("-" * 21)
            for scenario_name, data in self.results['worst_case'].items():
                report.append(f"  {scenario_name.replace('_', ' ').title()}:")
                report.append(f"    Insert: {data['insert_time']:.4f}s")
                report.append(f"    Search: {data['search_time']:.4f}s")
            report.append("")
        
        # Comparison with built-in structures
        if 'comparison' in self.results:
            comp = self.results['comparison']
            report.append("COMPARISON WITH BUILT-IN STRUCTURES:")
            report.append("-" * 37)
            report.append(f"  TST    - Insert: {comp['tst_insert']:.4f}s, Search: {comp['tst_search']:.4f}s")
            report.append(f"  Set    - Insert: {comp['set_insert']:.4f}s, Search: {comp['set_search']:.4f}s")
            report.append(f"  List   - Insert: {comp['list_insert']:.4f}s, Search: {comp['list_search']:.4f}s")
            report.append("")
        
        # Save results to a JSON file for analysis script
        json_path = "benchmark_results.json"
        with open(json_path, 'w') as f:
            json.dump(self.results, f, indent=4)
        print(f"  Saved raw results to '{json_path}'")
        
        # Save report to a text file
        report_path = "tst_performance_report.txt"
        with open(report_path, 'w') as f:
            f.write("\n".join(report))
        
        print(f"  Saved performance report to '{report_path}'")

def run_all_benchmarks(word_source='file'):
    """Main function to run all benchmark tests."""
    benchmark = TSTBenchmark()
    
    if word_source == 'file':
        words_to_insert = benchmark.load_words_from_file('corncob_lowercase.txt')
    else:
        # Fallback to random word generation
        words_to_insert = benchmark.generate_random_words(50000)

    # Run insert benchmark
    benchmark.benchmark_insert_performance(words_to_insert)
    
    # Run search benchmark
    benchmark.benchmark_search_performance(words_to_insert)
    
    # Run worst case scenarios benchmark
    benchmark.benchmark_worst_case_scenarios()
    
    # Compare with built-in structures
    benchmark.compare_with_builtin_structures(len(words_to_insert))
    
    # Create plots and generate textual report
    benchmark.create_performance_plots()
    benchmark.generate_report()

if __name__ == "__main__":
    run_all_benchmarks()
