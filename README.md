# Mini-Infer: High-Performance LLM Inference Engine 🚀

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![CUDA](https://img.shields.io/badge/CUDA-11.8+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Triton](https://img.shields.io/badge/Triton-2.1+-orange.svg)

**A lightweight yet powerful LLM inference engine with PagedAttention**

**基于PagedAttention的轻量级高性能大模型推理引擎**

*Inspired by vLLM, optimized for learning and performance*

[English](#english) | [中文](#chinese)

</div>

---

<a name="english"></a>

## 🌟 Features

### Core Capabilities

- ⚡ **High Performance**: Target 85-90% of vLLM throughput
- 💾 **Memory Efficient**: PagedAttention-based KV Cache management
- 🔧 **Custom Kernels**: Optimized Triton implementations (5-8x faster than PyTorch)
- 📊 **Continuous Batching**: Dynamic request scheduling for better throughput
- 🎯 **Well-Tested**: Comprehensive unit tests (target 85%+ coverage)

### Technical Highlights

```python
# Performance Targets
RMSNorm Kernel:      5-8x speedup vs PyTorch
Memory Utilization:  85%+ (PagedAttention)
End-to-End:          80-90% of vLLM performance
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/mini-infer.git
cd mini-infer

# Create virtual environment
conda create -n mini-infer python=3.10
conda activate mini-infer

# Install dependencies (coming soon)
pip install -r requirements.txt
```

### Basic Usage (Preview)

```python
from mini_infer import LLMEngine
from mini_infer.config import EngineConfig

# Initialize engine
config = EngineConfig(
    model="meta-llama/Llama-2-7b-hf",
    max_num_seqs=64,
    block_size=16
)
engine = LLMEngine(config)

# Generate
prompts = ["Hello, how are you?"]
outputs = engine.generate(prompts, max_tokens=100)
print(outputs[0].text)
```

---

## 📊 Performance Benchmarks (Coming Soon)

### Target Performance

| Component | Baseline | Mini-Infer | Target Speedup |
|-----------|----------|------------|----------------|
| RMSNorm Kernel | PyTorch | Triton | 5-8x |
| RoPE Kernel | PyTorch | Triton | 6-8x |
| Memory Util | 40% | PagedAttention | 85%+ |
| Throughput | Static Batch | Continuous Batch | 2-3x |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│         LLM Engine                  │
├─────────────────────────────────────┤
│  ┌──────────┐    ┌──────────┐      │
│  │Scheduler │───▶│Model     │      │
│  │(C-Batch) │    │Runner    │      │
│  └──────────┘    └──────────┘      │
├─────────────────────────────────────┤
│     Memory Management               │
│  ┌──────────────────────────┐      │
│  │  Block Manager           │      │
│  │  (PagedAttention)        │      │
│  └──────────────────────────┘      │
├─────────────────────────────────────┤
│     Custom Kernels (Triton)         │
│  ┌───────┐ ┌────┐ ┌──────────┐    │
│  │RMSNorm│ │RoPE│ │Attention │    │
│  └───────┘ └────┘ └──────────┘    │
└─────────────────────────────────────┘
```

---

## 📈 Roadmap

### Phase 1: Foundation (Weeks 1-2) ✅

- [x] Project structure
- [x] Basic documentation
- [ ] Development environment setup

### Phase 2: Core Implementation (Weeks 3-8)

- [ ] Triton kernels (RMSNorm, RoPE)
- [ ] PagedAttention Block Manager
- [ ] Continuous Batching Scheduler
- [ ] End-to-end inference engine

### Phase 3: Performance & Testing (Weeks 9-10)

- [ ] Comprehensive benchmarks
- [ ] Unit tests (85%+ coverage)
- [ ] Performance optimization

### Phase 4: Documentation & Polish (Weeks 11-12)

- [ ] API documentation
- [ ] Usage examples
- [ ] Technical blog posts

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

This project is inspired by and learns from:

- [vLLM](https://github.com/vllm-project/vllm) - PagedAttention and continuous batching
- [FlashAttention](https://github.com/Dao-AILab/flash-attention) - Efficient attention mechanisms
- [Triton](https://github.com/openai/triton) - GPU programming framework

---

<a name="chinese"></a>

## 🌟 核心特性

### 主要功能

- ⚡ **高性能**: 目标达到vLLM 85-90%的吞吐量
- 💾 **显存优化**: 基于PagedAttention的KV Cache管理
- 🔧 **自定义算子**: 优化的Triton实现 (比PyTorch快5-8倍)
- 📊 **连续批处理**: 动态请求调度，提升吞吐量
- 🎯 **测试完善**: 完整的单元测试 (目标覆盖率85%+)

### 技术亮点

```python
# 性能目标
RMSNorm算子:     相比PyTorch加速5-8倍
显存利用率:       85%+ (PagedAttention)
端到端性能:       vLLM的80-90%
```

---

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/mini-infer.git
cd mini-infer

# 创建虚拟环境
conda create -n mini-infer python=3.10
conda activate mini-infer

# 安装依赖 (即将推出)
pip install -r requirements.txt
```

### 基础使用 (预览)

```python
from mini_infer import LLMEngine
from mini_infer.config import EngineConfig

# 初始化引擎
config = EngineConfig(
    model="meta-llama/Llama-2-7b-hf",
    max_num_seqs=64,
    block_size=16
)
engine = LLMEngine(config)

# 生成文本
prompts = ["你好，最近怎么样？"]
outputs = engine.generate(prompts, max_tokens=100)
print(outputs[0].text)
```

---

## 📊 性能基准测试 (即将推出)

### 目标性能

| 组件 | 基准 | Mini-Infer | 目标加速比 |
|------|------|------------|-----------|
| RMSNorm算子 | PyTorch | Triton | 5-8x |
| RoPE算子 | PyTorch | Triton | 6-8x |
| 显存利用率 | 40% | PagedAttention | 85%+ |
| 吞吐量 | 静态批处理 | 连续批处理 | 2-3x |

---

## 📈 开发路线图

### 阶段1: 基础建设 (第1-2周) ✅

- [x] 项目结构
- [x] 基础文档
- [ ] 开发环境配置

### 阶段2: 核心实现 (第3-8周)

- [ ] Triton算子 (RMSNorm, RoPE)
- [ ] PagedAttention块管理器
- [ ] 连续批处理调度器
- [ ] 端到端推理引擎

### 阶段3: 性能与测试 (第9-10周)

- [ ] 完整的基准测试
- [ ] 单元测试 (覆盖率85%+)
- [ ] 性能优化

### 阶段4: 文档与完善 (第11-12周)

- [ ] API文档
- [ ] 使用示例
- [ ] 技术博客

---

## 🤝 贡献指南

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

---

## 📄 开源协议

本项目采用MIT协议 - 详见 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

本项目受以下优秀开源项目启发：

- [vLLM](https://github.com/vllm-project/vllm) - PagedAttention和连续批处理
- [FlashAttention](https://github.com/Dao-AILab/flash-attention) - 高效注意力机制
- [Triton](https://github.com/openai/triton) - GPU编程框架

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给个Star! ⭐**

**⭐ If you find this project helpful, please star it! ⭐**

</div>
