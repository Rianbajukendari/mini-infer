# Installation Guide | 安装指南

## Prerequisites | 前置要求

### Hardware Requirements | 硬件要求

**Minimum | 最低要求:**

- NVIDIA GPU with compute capability 7.0+ (V100, T4, or newer)
- 16GB GPU memory (for 7B models)
- 32GB system RAM

**Recommended | 推荐配置:**

- NVIDIA A100, A6000, or RTX 4090
- 40GB+ GPU memory
- 64GB+ system RAM

### Software Requirements | 软件要求

- **Operating System | 操作系统:** Linux (Ubuntu 20.04+recommended) or Windows with WSL2
- **Python:** 3.10 or 3.11
- **CUDA:** 11.8 or 12.1+
- **Driver:** NVIDIA  Driver 525.60.13+ (for CUDA 12.x)

---

## Installation Methods | 安装方法

### Method 1: From Source (Recommended) | 从源码安装（推荐）

#### Step 1: Clone Repository | 克隆仓库

```bash
git clone https://github.com/psmarter/mini-infer.git
cd mini-infer
```

#### Step 2: Create Virtual Environment | 创建虚拟环境

**Using Conda (Recommended) | 使用Conda（推荐）:**

```bash
conda create -n mini-infer python=3.10
conda activate mini-infer
```

**Using venv:**

```bash
python3.10 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Step 3: Install CUDA Toolkit | 安装CUDA工具包

**Conda (Easiest) | Conda（最简单）:**

```bash
conda install nvidia/label/cuda-11.8.0::cuda-toolkit
```

**Manual Installation | 手动安装:**

Download from [NVIDIA CUDA Downloads](https://developer.nvidia.com/cuda-downloads)

从 [NVIDIA CUDA下载](https://developer.nvidia.com/cuda-downloads) 下载

#### Step 4: Install PyTorch | 安装PyTorch

**For CUDA 11.8:**

```bash
pip install torch==2.0.1 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**For CUDA 12.1:**

```bash
pip install torch==2.1.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

#### Step 5: Install Triton | 安装Triton

```bash
pip install triton==2.1.0
```

#### Step 6: Install Mini-Infer | 安装Mini-Infer

**Development Mode (for contributing) | 开发模式（用于贡献）:**

```bash
pip install -e ".[dev]"
```

**Standard Installation | 标准安装:**

```bash
pip install -e .
```

**With benchmarking tools | 包含基准测试工具:**

```bash
pip install -e ".[all]"
```

---

### Method 2: Using pip (When Available) | 使用pip（可用时）

> [!NOTE]
> PyPI package will be available after the first stable release.
>
> PyPI包将在第一个稳定版本后可用。

```bash
pip install mini-infer
```

---

## Verify Installation | 验证安装

### Check CUDA Availability | 检查CUDA可用性

```python
import torch

print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
print(f"GPU device: {torch.cuda.get_device_name(0)}")
```

Expected output | 预期输出:

```
PyTorch version: 2.0.1
CUDA available: True
CUDA version: 11.8
GPU device: NVIDIA A100-SXM4-40GB
```

### Check Triton Installation | 检查Triton安装

```python
import triton
print(f"Triton version: {triton.__version__}")
```

### Run Tests | 运行测试

```bash
pytest tests/test_utils.py -v
```

---

## Common Issues | 常见问题

### Issue 1: CUDA Not Found | CUDA未找到

**Error | 错误:**

```
RuntimeError: CUDA driver version is insufficient for CUDA runtime version
```

**Solution | 解决方案:**

1. Update NVIDIA driver | 更新NVIDIA驱动:

   ```bash
   # Ubuntu
   sudo ubuntu-drivers autoinstall
   ```

2. Verify installation | 验证安装:

   ```bash
   nvidia-smi
   ```

---

### Issue 2: Triton Compilation Error | Triton编译错误

**Error | 错误:**

```
RuntimeError: Triton Error: failed to compile kernel
```

**Solution | 解决方案:**

1. Ensure CUDA toolkit is in PATH | 确保CUDA工具包在PATH中:

   ```bash
   export PATH=/usr/local/cuda/bin:$PATH
   export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
   ```

2. Reinstall Triton | 重新安装Triton:

   ```bash
   pip uninstall triton
   pip install triton==2.1.0
   ```

---

### Issue 3: Out of Memory | 内存不足

**Error | 错误:**

```
torch.cuda.OutOfMemoryError: CUDA out of memory
```

**Solutions | 解决方案:**

1. Reduce batch size in config | 减少配置中的批量大小:

   ```python
   config = EngineConfig(
       model="...",
       max_num_seqs=32,  # Reduce from 64
       gpu_memory_utilization=0.85  # Reduce from 0.9
   )
   ```

2. Use smaller model | 使用更小的模型:
   - Try 3B or 7B models instead of 13B+
   - 尝试3B或7B模型而不是13B+

3. Clear CUDA cache | 清除CUDA缓存:

   ```python
   import torch
   torch.cuda.empty_cache()
   ```

---

### Issue 4: Import Error | 导入错误

**Error | 错误:**

```
ModuleNotFoundError: No module named 'mini_infer'
```

**Solution | 解决方案:**

Ensure you installed in editable mode | 确保以可编辑模式安装:

```bash
cd /path/to/mini-infer
pip install -e .
```

---

## Development Setup | 开发环境设置

### Install Development Dependencies | 安装开发依赖

```bash
pip install -e ".[dev]"
```

### Install Pre-commit Hooks | 安装Pre-commit钩子

```bash
pre-commit install
```

### Run Code Quality Checks | 运行代码质量检查

```bash
# Format code
black mini_infer/ tests/

# Sort imports
isort mini_infer/ tests/

# Lint
flake8 mini_infer/ tests/

# Type check
mypy mini_infer/
```

### Run All Tests | 运行所有测试

```bash
# All tests
pytest

# With coverage
pytest --cov=mini_infer --cov-report=html

# Only fast tests
pytest -m "not slow and not gpu"
```

---

## Docker Installation (Coming Soon) | Docker安装（即将推出）

> [!NOTE]
> Docker support will be added in a future release.
>
> Docker支持将在未来版本中添加。

```bash
# Pull image
docker pull psmarter/mini-infer:latest

# Run
docker run --gpus all -it psmarter/mini-infer:latest
```

---

## Environment Variables | 环境变量

Optional environment variables for configuration:

用于配置的可选环境变量：

```bash
# CUDA device selection
export CUDA_VISIBLE_DEVICES=0,1

# Triton cache directory
export TRITON_CACHE_DIR=/tmp/triton_cache

# Enable Triton debugging
export TRITON_DEBUG=1

# HuggingFace cache directory
export HF_HOME=/path/to/cache
```

---

## Upgrading | 升级

### Upgrade from Git | 从Git升级

```bash
cd mini-infer
git pull origin main
pip install -e . --upgrade
```

### Upgrade from pip (When Available) | 从pip升级（可用时）

```bash
pip install --upgrade mini-infer
```

---

## Uninstallation | 卸载

```bash
pip uninstall mini-infer
```

To remove all associated files | 删除所有相关文件:

```bash
# Remove conda environment
conda remove -n mini-infer --all

# Or remove venv
rm -rf venv/
```

---

## Next Steps | 下一步

After installation, check out:

安装后，查看：

- [Quick Start Guide](file:///h:/就业/mini-infer/README.md#quick-start) - Basic usage examples
- [API Reference](file:///h:/就业/mini-infer/docs/api_reference.md) - Detailed API documentation
- [Architecture](file:///h:/就业/mini-infer/docs/architecture.md) - System design overview
- [Examples](file:///h:/就业/mini-infer/examples) - Code examples

---

## Getting Help | 获取帮助

If you encounter issues:

如果遇到问题：

1. Check [FAQ](file:///h:/就业/mini-infer/docs/faq.md)
2. Search [existing issues](https://github.com/psmarter/mini-infer/issues)
3. Open a [new issue](https://github.com/psmarter/mini-infer/issues/new/choose)
4. Join discussions (coming soon)
