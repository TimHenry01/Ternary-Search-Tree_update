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

# Add the parent directory to the path to import our module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ternary_search_tree import TernarySearchTree


class TSTBenchmark:
    """Comprehensive benchmarking suite for Ternary Search Tree."""
    
    def __init__(self):
        self.results = defaultdict(list)
        
    def generate_random_words(self, count, min_length=3, max_length=10):
        """Generate random words for testing."""
        words = []
        for _ in range(count):
            length = random.randint(min_length, max_length)
            word = ''.join(random.choices(string.ascii_lowercase, k=length))
            words.append(word)
        return list(set(words))  # Remove duplicates
    
    def generate_sequential_words(self, count):
        """Generate sequential words (worst case for some operations)."""
        return [f"word{i:06d}" for i in range(count)]
    
    def generate_similar_words(self, count, base="test"):
        """Generate words with similar prefixes (specific case analysis)."""
        words = [base]
        for i in range(1, count):
            suffix = ''.join(random.choices(string.ascii_lowercase, k=random.randint(1, 5)))
            words.append(f"{base}{suffix}")
        return words
    
    def benchmark_insert_performance(self, word_counts=[100, 500, 1000, 2000, 5000, 10000]):
        """Benchmark insert operation performance scaling."""
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
            self.results['insert_counts'].append(count)
            self.results['insert_times'].append(insert_time)
            self.results['insert_memory'].append(peak / 1024 / 1024)
            
            print(f"    Time: {insert_time:.4f}s, Memory: {peak/1024/1024:.2f}MB")
        
        return word_counts, insert_times, memory_usage
    
    def benchmark_search_performance(self, word_counts=[100, 500, 1000, 2000, 5000, 10000]):
        """Benchmark search operation performance scaling."""
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
            self.results['search_counts'].append(count)
            self.results['search_times'].append(search_time)
            
            print(f"    Time: {search_time:.4f}s")
        
        return word_counts, search_times
    
    def benchmark_worst_case_scenarios(self):
        """Test worst-case scenarios for TST operations."""
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
            
            # Store results (height calls removed)
            self.results[f'worst_case_{scenario_name}_insert'] = insert_time
            self.results[f'worst_case_{scenario_name}_search'] = search_time
            
            print(f"    Insert: {insert_time:.4f}s, Search: {search_time:.4f}s")
    
    def compare_with_builtin_structures(self, word_count=5000):
        """Compare TST performance with Python's built-in data structures."""
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
    
    def create_performance_plots(self):
        """Create performance visualization plots."""
        print("Creating performance plots...")
        
        # Create subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Insert performance plot
        if 'insert_counts' in self.results:
            ax1.plot(self.results['insert_counts'], self.results['insert_times'], 'bo-', label='Insert Time')
            ax1.set_xlabel('Number of Words')
            ax1.set_ylabel('Time (seconds)')
            ax1.set_title('Insert Performance Scaling')
            ax1.grid(True)
            ax1.legend()
        
        # Search performance plot
        if 'search_counts' in self.results:
            ax2.plot(self.results['search_counts'], self.results['search_times'], 'ro-', label='Search Time')
            ax2.set_xlabel('Number of Words')
            ax2.set_ylabel('Time (seconds)')
            ax2.set_title('Search Performance Scaling')
            ax2.grid(True)
            ax2.legend()
        
        # Memory usage plot
        if 'insert_memory' in self.results:
            ax3.plot(self.results['insert_counts'], self.results['insert_memory'], 'go-', label='Memory Usage')
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
    
    def generate_report(self):
        """Generate a comprehensive performance report."""
        print("\nGenerating performance report...")
        
        report = []
        report.append("=" * 60)
        report.append("TERNARY SEARCH TREE PERFORMANCE ANALYSIS REPORT")
        report.append("=" * 60)
        report.append("")
        
        # Insert performance analysis
        if 'insert_times' in self.results:
            report.append("INSERT PERFORMANCE:")
            report.append("-" * 20)
            for i, (count, time_taken) in enumerate(zip(self.results['insert_counts'], self.results['insert_times'])):
                rate = count / time_taken if time_taken > 0 else float('inf')
                report.append(f"  {count:5d} words: {time_taken:.4f}s ({rate:.0f} words/sec)")
            report.append("")
        
        # Search performance analysis
        if 'search_times' in self.results:
            report.append("SEARCH PERFORMANCE:")
            report.append("-" * 19)
            for count, time_taken in zip(self.results['search_counts'], self.results['search_times']):
                rate = count / time_taken if time_taken > 0 else float('inf')
                report.append(f"  {count:5d} words: {time_taken:.4f}s ({rate:.0f} searches/sec)")
            report.append("")
        
        # Worst case scenarios - skipping height since you removed it
        worst_cases = [key for key in self.results.keys() if key.startswith('worst_case_')]
        if worst_cases:
            report.append("WORST CASE SCENARIOS:")
            report.append("-" * 21)
            scenarios = set(key.split('_')[2] for key in worst_cases if '_insert' in key)
            for scenario in scenarios:
                insert_key = f'worst_case_{scenario}_insert'
                search_key = f'worst_case_{scenario}_search'
                if insert_key in self.results and search_key in self.results:
                    report.append(f"  {scenario.replace('_', ' ').title()}:")
                    report.append(f"    Insert: {self.results[insert_key]:.4f}s")
                    report.append(f"    Search: {self.results[search_key]:.4f}s")
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
        
        # Theoretical complexity (optional)
        report.append("THEORETICAL COMPLEXITY ANALYSIS:")
        report.append("-" * 32)
        report.append("  Insert:")
        report.append("    Best case:    O(log n)")
        report.append("    Average case: O(log n)")
        report.append("    Worst case:   O(n)")
        report.append("  Search:")
        report.append("    Best case:    O(log n)")
        report.append("    Average case: O(log n)")
        report.append("    Worst case:   O(n)")
        report.append("")
        report.append("NOTES:")
        report.append("- Insert/search times are influenced by input distribution.")
        report.append("- Memory usage is measured using tracemalloc and may vary per run.")
        report.append("- List structure suffers on search due to linear lookup time.")
        report.append("- TST is optimized for prefix and near-prefix retrievals.")
        report.append("")
        
        # Save report to file
        report_path = "tst_performance_report.txt"
        with open(report_path, 'w') as f:
            f.write("\n".join(report))
        
        print(f"  Saved performance report to '{report_path}'")


if __name__ == "__main__":
    benchmark = TSTBenchmark()
    
    # Run insert benchmark
    benchmark.benchmark_insert_performance()
    
    # Run search benchmark
    benchmark.benchmark_search_performance()
    
    # Run worst case scenarios benchmark
    benchmark.benchmark_worst_case_scenarios()
    
    # Compare with built-in structures
    benchmark.compare_with_builtin_structures()
    
    # Create plots
    benchmark.create_performance_plots()
    
    # Generate textual report
    benchmark.generate_report()
