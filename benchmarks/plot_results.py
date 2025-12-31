"""
Visualization Script for Benchmark Results

This script generates charts and visualizations from benchmark data.

Usage:
    python benchmarks/plot_results.py
"""

import json
from pathlib import Path
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 11


def plot_throughput_comparison(data_path: Path, output_path: Path):
    """Generate throughput comparison chart"""
    
    if not data_path.exists():
        print(f"⚠️  Warning: {data_path} not found. Skipping throughput plot.")
        return
    
    # Load data
    with open(data_path) as f:
        data = json.load(f)
    
    # Prepare data for plotting
    batch_sizes = [int(bs) for bs in data.keys()]
    throughputs = [data[str(bs)]["throughput_tokens_per_sec"] for bs in batch_sizes]
    
    # Create plot
    fig, ax = plt.subplots(figsize=(12, 6))
    
    colors = sns.color_palette("viridis", len(batch_sizes))
    bars = ax.bar(range(len(batch_sizes)), throughputs, color=colors, alpha=0.8, edgecolor='black')
    
    # Customize plot
    ax.set_xlabel("Batch Size", fontsize=13, fontweight='bold')
    ax.set_ylabel("Throughput (tokens/s)", fontsize=13, fontweight='bold')
    ax.set_title("Mini-Infer Throughput vs Batch Size", fontsize=15, fontweight='bold', pad=20)
    ax.set_xticks(range(len(batch_sizes)))
    ax.set_xticklabels(batch_sizes)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels on bars
    for i, (bar, throughput) in enumerate(zip(bars, throughputs)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{throughput:.0f}',
               ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Save
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {output_path}")
    plt.close()


def plot_latency_distribution(data_path: Path, output_path: Path):
    """Generate latency percentile chart"""
    
    if not data_path.exists():
        print(f"⚠️  Warning: {data_path} not found. Skipping latency plot.")
        return
    
    # Load data
    with open(data_path) as f:
        data = json.load(f)
    
    # Prepare data
    percentiles = ['p50_ms', 'p90_ms', 'p95_ms', 'p99_ms']
    percentile_labels = ['P50', 'P90', 'P95', 'P99']
    values = [data[p] for p in percentiles]
    
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = ['#2ecc71', '#f39c12', '#e74c3c', '#c0392b']
    bars = ax.bar(percentile_labels, values, color=colors, alpha=0.8, edgecolor='black')
    
    # Customize plot
    ax.set_xlabel("Percentile", fontsize=13, fontweight='bold')
    ax.set_ylabel("Latency (ms)", fontsize=13, fontweight='bold')
    ax.set_title("Mini-Infer Latency Distribution", fontsize=15, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels on bars
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{value:.1f}ms',
               ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Add mean and median lines
    if 'mean_ms' in data:
        ax.axhline(y=data['mean_ms'], color='blue', linestyle='--', 
                  linewidth=2, alpha=0.7, label=f"Mean: {data['mean_ms']:.1f}ms")
    if 'median_ms' in data:
        ax.axhline(y=data['median_ms'], color='green', linestyle='--', 
                  linewidth=2, alpha=0.7, label=f"Median: {data['median_ms']:.1f}ms")
    
    ax.legend(loc='upper left', fontsize=10)
    
    # Save
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {output_path}")
    plt.close()


def plot_combined_overview(throughput_path: Path, latency_path: Path, output_path: Path):
    """Generate combined overview chart"""
    
    # Check if both files exist
    if not throughput_path.exists() or not latency_path.exists():
        print(f"⚠️  Warning: Missing data files. Skipping combined plot.")
        return
    
    # Load data
    with open(throughput_path) as f:
        throughput_data = json.load(f)
    with open(latency_path) as f:
        latency_data = json.load(f)
    
    # Create subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot 1: Throughput
    batch_sizes = [int(bs) for bs in throughput_data.keys()]
    throughputs = [throughput_data[str(bs)]["throughput_tokens_per_sec"] for bs in batch_sizes]
    
    colors1 = sns.color_palette("viridis", len(batch_sizes))
    ax1.bar(range(len(batch_sizes)), throughputs, color=colors1, alpha=0.8, edgecolor='black')
    ax1.set_xlabel("Batch Size", fontsize=12, fontweight='bold')
    ax1.set_ylabel("Throughput (tokens/s)", fontsize=12, fontweight='bold')
    ax1.set_title("Throughput vs Batch Size", fontsize=13, fontweight='bold')
    ax1.set_xticks(range(len(batch_sizes)))
    ax1.set_xticklabels(batch_sizes)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Plot 2: Latency
    percentile_labels = ['P50', 'P90', 'P95', 'P99']
    percentiles = ['p50_ms', 'p90_ms', 'p95_ms', 'p99_ms']
    values = [latency_data[p] for p in percentiles]
    
    colors2 = ['#2ecc71', '#f39c12', '#e74c3c', '#c0392b']
    ax2.bar(percentile_labels, values, color=colors2, alpha=0.8, edgecolor='black')
    ax2.set_xlabel("Percentile", fontsize=12, fontweight='bold')
    ax2.set_ylabel("Latency (ms)", fontsize=12, fontweight='bold')
    ax2.set_title("Latency Distribution", fontsize=13, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Overall title
    fig.suptitle("Mini-Infer Performance Overview", fontsize=16, fontweight='bold', y=1.02)
    
    # Save
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {output_path}")
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Plot benchmark results")
    parser.add_argument(
        "--throughput-data",
        type=str,
        default="benchmarks/results/throughput.json",
        help="Path to throughput data JSON"
    )
    parser.add_argument(
        "--latency-data",
        type=str,
        default="benchmarks/results/latency.json",
        help="Path to latency data JSON"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="benchmarks/results",
        help="Output directory for charts"
    )
    
    args = parser.parse_args()
    
    throughput_path = Path(args.throughput_data)
    latency_path = Path(args.latency_data)
    output_dir = Path(args.output_dir)
    
    print(f"\n{'='*60}")
    print("Generating Benchmark Visualizations")
    print(f"{'='*60}\n")
    
    # Generate plots
    plot_throughput_comparison(
        throughput_path,
        output_dir / "throughput_chart.png"
    )
    
    plot_latency_distribution(
        latency_path,
        output_dir / "latency_chart.png"
    )
    
    plot_combined_overview(
        throughput_path,
        latency_path,
        output_dir / "performance_overview.png"
    )
    
    print(f"\n{'='*60}")
    print("✅ All visualizations generated successfully!")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
