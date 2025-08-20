#!/bin/bash
#SBATCH --job-name=tst_benchmark
#SBATCH --output=tst_benchmark_%j.out
#SBATCH --error=tst_benchmark_%j.err
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8GB
#SBATCH --partition=batch

# TST Performance Benchmarking Job Script
# This script runs comprehensive performance tests for the Ternary Search Tree implementation

echo "========================================"
echo "TST BENCHMARK JOB STARTED"
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURMD_NODENAME"
echo "Start Time: $(date)"
echo "========================================"

# Load required modules (adjust based on your HPC environment)
module purge
module load cluster/genius/batch
module load Python/3.13.1-GCCcore-14.2.0
# module load matplotlib/3.5.2-foss-2022a  # Uncomment if needed
# module load numpy/1.21.3-foss-2022a      # Uncomment if needed

# Set up Python environment
export PYTHONPATH=$PYTHONPATH:$PWD

# Ensure we start from the submission directory
cd $SLURM_SUBMIT_DIR || { echo "Failed to cd to SLURM_SUBMIT_DIR"; exit 1; }

# Create output directory for results
mkdir -p benchmark_results

# Copy benchmark files to results directory
cp *.py benchmark_results/

# Move into benchmark_results directory to run benchmarks and save outputs there
cd benchmark_results || { echo "Failed to cd into benchmark_results"; exit 1; }

echo "Installing required Python packages..."
pip install --user matplotlib numpy

echo "========================================"
echo "RUNNING TST CORRECTNESS TESTS"
echo "========================================"

# Run unit tests first to ensure correctness
python test_ternary_search_tree.py

if [ $? -eq 0 ]; then
    echo "All tests passed! Proceeding with benchmarks..."
else
    echo "Tests failed! Stopping benchmark execution."
    exit 1
fi

echo "========================================"
echo "RUNNING PERFORMANCE BENCHMARKS"
echo "========================================"

# Run the full benchmark suite
python benchmark_tst.py

echo "========================================"
echo "RUNNING ADDITIONAL LARGE-SCALE TESTS"
echo "========================================"

# Create and run additional large-scale benchmarks
cat > large_scale_benchmark.py << 'EOF'
"""
Large-scale benchmarking specifically for HPC environment.
Tests with larger datasets than typical local testing.
"""

import sys
sys.path.append('.')

from benchmark_tst import TSTBenchmark
import time

def hpc_large_scale_tests():
    """Run large-scale tests optimized for HPC environment."""
    print("Starting HPC-specific large-scale benchmarks...")
    
    benchmark = TSTBenchmark()
    
    # Test with much larger datasets
    large_counts = [1000, 5000, 10000, 25000, 50000]
    
    print("Large-scale insert performance test...")
    benchmark.benchmark_insert_performance(large_counts)
    
    print("Large-scale search performance test...")
    benchmark.benchmark_search_performance(large_counts)
    
    # Memory stress test
    print("Memory stress test with 100,000 words...")
    words = benchmark.generate_random_words(100000)
    
    start_time = time.perf_counter()
    tst = benchmark.TernarySearchTree()
    
    for i, word in enumerate(words):
        tst.insert(word)
        if (i + 1) % 10000 == 0:
            print(f"  Inserted {i + 1} words...")
    
    insert_time = time.perf_counter() - start_time
    print(f"Total insert time for 100k words: {insert_time:.2f}s")
    
    # Search all words
    start_time = time.perf_counter()
    for word in words:
        assert tst.search(word), f"Failed to find word: {word}"
    search_time = time.perf_counter() - start_time
    print(f"Total search time for 100k words: {search_time:.2f}s")
    
    print(f"Final tree stats: {len(tst)} words, height: {tst.height()}")
    
    # Generate final report
    benchmark.generate_report()
    benchmark.create_performance_plots()

if __name__ == '__main__':
    hpc_large_scale_tests()
EOF

python large_scale_benchmark.py

echo "========================================"
echo "COLLECTING SYSTEM INFORMATION"
echo "========================================"

# Collect system information for the report
cat > system_info.txt << EOF
HPC Benchmark System Information
================================
Job ID: $SLURM_JOB_ID
Node: $SLURMD_NODENAME
Date: $(date)
Python Version: $(python --version)
CPU Info: $(lscpu | grep "Model name" || echo "CPU info not available")
Memory Info: $(free -h | head -2 || echo "Memory info not available")
Load Average: $(uptime)
EOF

echo "System information:"
cat system_info.txt

echo "========================================"
echo "BENCHMARK RESULTS SUMMARY"
echo "========================================"

# Display key result files
echo "Generated files:"
ls -la *.png *.txt *.out 2>/dev/null || echo "No output files found"

if [ -f "tst_performance_report.txt" ]; then
    echo ""
    echo "Performance Report Summary:"
    echo "---------------------------"
    head -50 tst_performance_report.txt
fi

echo "========================================"
echo "TST BENCHMARK JOB COMPLETED"
echo "End Time: $(date)"
echo "========================================"

# Copy results back to submission directory
cp *.png *.txt *.out ../ 2>/dev/null || true

echo "All benchmark results have been saved to the job output directory."
