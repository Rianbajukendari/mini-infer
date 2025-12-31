# Benchmarks

This directory contains benchmark scripts and results for Mini-Infer performance evaluation.

## 📁 Structure

```
benchmarks/
├── benchmark_throughput.py    # Throughput benchmark script
├── benchmark_latency.py       # Latency benchmark script
├── plot_results.py            # Visualization script
└── results/                   # Benchmark results and charts
    ├── throughput.json
    ├── latency.json
    ├── throughput_chart.png
    ├── latency_chart.png
    └── performance_overview.png
```

## 🚀 Quick Start

### 1. Run Throughput Benchmark

```bash
# Basic usage (with mock engine)
python benchmarks/benchmark_throughput.py

# With custom parameters
python benchmarks/benchmark_throughput.py \
    --model meta-llama/Llama-2-7b-hf \
    --batch-sizes 1 8 16 32 64 \
    --num-prompts 100 \
    --max-tokens 128
```

### 2. Run Latency Benchmark

```bash
# Basic usage (with mock engine)
python benchmarks/benchmark_latency.py

# With custom parameters
python benchmarks/benchmark_latency.py \
    --model meta-llama/Llama-2-7b-hf \
    --num-runs 200 \
    --max-tokens 50
```

### 3. Generate Visualizations

```bash
# Generate all charts
python benchmarks/plot_results.py

# With custom paths
python benchmarks/plot_results.py \
    --throughput-data benchmarks/results/throughput.json \
    --latency-data benchmarks/results/latency.json \
    --output-dir benchmarks/results
```

## 📊 Output Files

### JSON Results

**throughput.json** - Contains throughput data for different batch sizes:

```json
{
  "8": {
    "throughput_tokens_per_sec": 1050.5,
    "total_tokens": 12800,
    "elapsed_sec": 12.19,
    "num_prompts": 100,
    "avg_tokens_per_prompt": 128.0
  }
}
```

**latency.json** - Contains latency statistics:

```json
{
  "mean_ms": 45.2,
  "median_ms": 44.8,
  "p95_ms": 52.3,
  "p99_ms": 58.1,
  "num_runs": 100
}
```

### Charts

- `throughput_chart.png` - Bar chart showing throughput vs batch size
- `latency_chart.png` - Bar chart showing latency percentiles
- `performance_overview.png` - Combined overview of both metrics

## 🔧 Customization

### Adding New Benchmarks

Create a new script following this template:

```python
"""
Your Benchmark Description
"""

import time
import json
from pathlib import Path

def benchmark_your_metric(model_name: str, **kwargs):
    """Your benchmark implementation"""
    # Initialize engine
    # Run tests
    # Collect metrics
    return results

if __name__ == "__main__":
    # Parse arguments
    # Run benchmark
    # Save results
    pass
```

### Integrating with Real Engine

Replace the mock implementations in the scripts:

```python
# Remove this:
from benchmarks.benchmark_throughput import MockLLMEngine

# Add this:
from mini_infer import LLMEngine
from mini_infer.config import EngineConfig
```

## 📈 Performance Targets

### Throughput Goals

| Batch Size | Target (tokens/s) |
|------------|-------------------|
| 8          | 400+              |
| 16         | 700+              |
| 32         | 1000+             |
| 64         | 1200+             |

### Latency Goals

| Metric | Target |
|--------|--------|
| P50    | < 30ms |
| P95    | < 50ms |
| P99    | < 70ms |

## 🤝 Contributing

When adding benchmarks:

1. Include clear documentation
2. Support command-line arguments
3. Save results in JSON format
4. Follow existing naming conventions
5. Add visualization support if applicable

## 📝 Notes

- **Current Status**: Scripts use mock implementations for development
- **Next Steps**: Integrate with actual Mini-Infer engine once core modules are complete
- **GPU Required**: Real benchmarks require CUDA-capable GPU
- **Dependencies**: See `requirements.txt` for visualization dependencies
