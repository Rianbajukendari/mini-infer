# Scripts

Helper scripts for Mini-Infer development and benchmarking.

## 📁 Scripts

### `setup_env.bat`

Sets up the development environment with all dependencies.

**Usage:**

```cmd
scripts\setup_env.bat
```

**What it does:**

- Creates conda environment `mini-infer`
- Installs PyTorch with CUDA 11.8
- Installs all dependencies from `requirements.txt`
- Installs Mini-Infer in development mode

### `run_benchmarks.bat`

Runs all benchmarks and generates visualizations.

**Usage:**

```cmd
scripts\run_benchmarks.bat
```

**What it does:**

- Runs throughput benchmark
- Runs latency benchmark
- Generates performance charts
- Saves results to `benchmarks/results/`

## 🔧 Requirements

- **Windows**: Scripts use `.bat` format
- **Conda**: Anaconda or Miniconda installed
- **CUDA** (optional): For GPU acceleration

## 📝 Notes

For Linux/Mac users, create equivalent `.sh` scripts:

- Replace `@echo off` with `#!/bin/bash`
- Replace `call conda` with `source activate`
- Replace backslashes with forward slashes in paths
