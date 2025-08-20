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
    def benchmark_insert_performance(self, word_counts=[100, 500, 1000, 2000, 5000, 10000]):
        print("Benchmarking insert performance...")
        
        insert_times = []
        memory_usage = []
        
        for count in word_counts:
            print(f"  Testing with {count} words...")
            
            # Generate test data
            words = self.generate_random_words(count)
            
            # Measure memory before
            tracemalloc.start()
            gc.collect()
            
            # Create TST and measure insert time
            tst = TernarySearchTree()
            start_time = time.perf_counter()
            
            for word in words:
                tst.insert(word)
            
            end_time = time.perf_counter()
            insert_time = end_time - start_time
            
            # Measure memory after
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            insert_times.append(insert_time)
            memory_usage.append(peak / 1024 / 1024)  # Convert to MB
            
            # Store results
            self.results['insert']['counts'].append(count)
            self.results['insert']['times'].append(insert_time)
            self.results['insert']['memory'].append(peak / 1024 / 1024)
            
            print(f"    Time: {insert_time:.4f}s, Memory: {peak/1024/1024:.2f}MB")
        
    # Benchmark search operation performance scaling.
    def benchmark_search_performance(self, word_counts=[100, 500, 1000, 2000, 5000, 10000]):
        print("Benchmarking search performance...")
        
        search_times = []
        
        for count in word_counts:
            print(f"  Testing with {count} words...")
            
            # Generate test data and build tree
            words = self.generate_random_words(count)
            tst = TernarySearchTree()
            
            for word in words:
                tst.insert(word)
            
            # Measure search time
            start_time = time.perf_counter()
            
            for word in words:
                tst.search(word)
            
            end_time = time.perf_counter()
            search_time = end_time - start_time
            
            search_times.append(search_time)
            
            # Store results
            self.results['search']['counts'].append(count)
            self.results['search']['times'].append(search_time)
            
            print(f"    Time: {search_time:.4f}s")
    
    # Test worst-case scenarios for TST operations.
    def benchmark_worst_case_scenarios(self):
        print("Benchmarking worst-case scenarios...")
        
        scenarios = {
            'sequential': self.generate_sequential_words(1000),
            'similar_prefixes': self.generate_similar_words(1000, "commonprefix"),
            'single_chars': [chr(i) for i in range(ord('a'), ord('z')+1)] * 40,
            'reverse_sorted': sorted(self.generate_random_words(1000), reverse=True)
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
            for word in words[:100]:  # Sample for search test
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
        for word in words:
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
    
    # Create performance visualization plots.
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
            for i, (count, time_taken) in enumerate(zip(self.results['insert']['counts'], self.results['insert']['times'])):
                rate = count / time_taken if time_taken > 0 else float('inf')
                report.append(f"  {count:5d} words: {time_taken:.4f}s ({rate:.0f} words/sec)")
            report.append("")
        
        # Search performance analysis
        if 'search' in self.results and self.results['search']:
            report.append("SEARCH PERFORMANCE:")
            report.append("-" * 19)
            for count, time_taken in zip(self.results['search']['counts'], self.results['search']['times']):
                rate = count / time_taken if time_taken > 0 else float('inf')
                report.append(f"  {count:5d} words: {time_taken:.4f}s ({rate:.0f} searches/sec)")
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

# Main function to run all benchmark tests.
def run_all_benchmarks():
    benchmark = TSTBenchmark()
    
    # Run insert benchmark
    benchmark.benchmark_insert_performance()
    
    # Run search benchmark
    benchmark.benchmark_search_performance()
    
    # Run worst case scenarios benchmark
    benchmark.benchmark_worst_case_scenarios()
    
    # Compare with built-in structures
    benchmark.compare_with_builtin_structures()
    
    # Create plots and generate textual report
    benchmark.create_performance_plots()
    benchmark.generate_report()

if __name__ == "__main__":
    run_all_benchmarks()
