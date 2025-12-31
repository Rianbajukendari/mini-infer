"""
Latency Benchmark Script for Mini-Infer

This script measures the per-request latency of Mini-Infer, including percentile statistics.
Results are saved in JSON format for later analysis.

Usage:
    python benchmarks/benchmark_latency.py
"""

import time
import json
from pathlib import Path
from typing import Dict, List
import argparse
import numpy as np

# Mock implementation - will be replaced with actual Mini-Infer imports
# from mini_infer import LLMEngine
# from mini_infer.config import EngineConfig


class MockLLMEngine:
    """Mock engine for testing - replace with actual implementation"""
    def __init__(self, config):
        self.config = config
        
    def generate(self, prompts: List[str], max_tokens: int = 50):
        # Simulate generation time with some randomness
        time.sleep(0.02 + np.random.random() * 0.03)
        return [{"text": "Generated response", "token_ids": list(range(max_tokens))}]


class MockEngineConfig:
    """Mock config for testing - replace with actual implementation"""
    def __init__(self, model: str, max_num_seqs: int = 1):
        self.model = model
        self.max_num_seqs = max_num_seqs


def benchmark_latency(
    model_name: str,
    num_runs: int = 100,
    max_tokens: int = 50,
    prompt: str = None
) -> Dict:
    """
    Benchmark per-request latency.
    
    Args:
        model_name: Model name or path
        num_runs: Number of requests to measure
        max_tokens: Maximum tokens to generate per request
        prompt: Test prompt (uses default if None)
    
    Returns:
        Dictionary containing latency statistics
    """
    
    if prompt is None:
        prompt = "Hello, how are you today? Please tell me about yourself."
    
    print(f"\n{'='*60}")
    print(f"Latency Benchmark")
    print(f"{'='*60}")
    print(f"Model: {model_name}")
    print(f"Number of runs: {num_runs}")
    print(f"Max tokens: {max_tokens}")
    print(f"Prompt: {prompt[:50]}...")
    print(f"{'='*60}\n")
    
    # Initialize engine (using mock for now)
    config = MockEngineConfig(model=model_name, max_num_seqs=1)
    engine = MockLLMEngine(config)
    
    # Warm up
    print("Warming up...")
    for _ in range(5):
        _ = engine.generate([prompt], max_tokens=max_tokens)
    
    # Benchmark
    print(f"Running {num_runs} iterations...")
    latencies = []
    
    for i in range(num_runs):
        if (i + 1) % 20 == 0:
            print(f"  Progress: {i + 1}/{num_runs}")
        
        start = time.time()
        _ = engine.generate([prompt], max_tokens=max_tokens)
        latency = (time.time() - start) * 1000  # Convert to ms
        latencies.append(latency)
    
    # Calculate statistics
    latencies_array = np.array(latencies)
    
    results = {
        "mean_ms": round(float(np.mean(latencies_array)), 2),
        "median_ms": round(float(np.median(latencies_array)), 2),
        "std_ms": round(float(np.std(latencies_array)), 2),
        "min_ms": round(float(np.min(latencies_array)), 2),
        "max_ms": round(float(np.max(latencies_array)), 2),
        "p50_ms": round(float(np.percentile(latencies_array, 50)), 2),
        "p90_ms": round(float(np.percentile(latencies_array, 90)), 2),
        "p95_ms": round(float(np.percentile(latencies_array, 95)), 2),
        "p99_ms": round(float(np.percentile(latencies_array, 99)), 2),
        "num_runs": num_runs,
        "max_tokens": max_tokens
    }
    
    return results


def save_results(results: Dict, output_path: Path):
    """Save benchmark results to JSON file"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Results saved to: {output_path}\n")


def print_results(results: Dict):
    """Print formatted results"""
    print(f"\n{'='*60}")
    print("Latency Statistics (milliseconds)")
    print(f"{'='*60}")
    print(f"Mean:     {results['mean_ms']:>8.2f} ms")
    print(f"Median:   {results['median_ms']:>8.2f} ms")
    print(f"Std Dev:  {results['std_ms']:>8.2f} ms")
    print(f"Min:      {results['min_ms']:>8.2f} ms")
    print(f"Max:      {results['max_ms']:>8.2f} ms")
    print(f"{'─'*60}")
    print("Percentiles:")
    print(f"  P50:    {results['p50_ms']:>8.2f} ms")
    print(f"  P90:    {results['p90_ms']:>8.2f} ms")
    print(f"  P95:    {results['p95_ms']:>8.2f} ms")
    print(f"  P99:    {results['p99_ms']:>8.2f} ms")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description="Benchmark Mini-Infer latency")
    parser.add_argument(
        "--model",
        type=str,
        default="meta-llama/Llama-2-7b-hf",
        help="Model name or path"
    )
    parser.add_argument(
        "--num-runs",
        type=int,
        default=100,
        help="Number of requests to measure"
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=50,
        help="Maximum tokens per request"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default=None,
        help="Test prompt (uses default if not specified)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="benchmarks/results/latency.json",
        help="Output JSON file path"
    )
    
    args = parser.parse_args()
    
    # Run benchmark
    results = benchmark_latency(
        model_name=args.model,
        num_runs=args.num_runs,
        max_tokens=args.max_tokens,
        prompt=args.prompt
    )
    
    # Print results
    print_results(results)
    
    # Save results
    output_path = Path(args.output)
    save_results(results, output_path)


if __name__ == "__main__":
    main()
