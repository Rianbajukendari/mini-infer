# Frequently Asked Questions | 常见问题

## General Questions | 一般问题

### What is Mini-Infer? | Mini-Infer是什么？

Mini-Infer is a high-performance LLM (Large Language Model) inference engine designed to achieve 85-90% of vLLM's throughput while maintaining code clarity for educational purposes. It implements PagedAttention for memory efficiency and custom Triton kernels for performance.

Mini-Infer是一个高性能LLM（大语言模型）推理引擎，旨在达到vLLM 85-90%的吞吐量，同时保持代码清晰以用于教育目的。它实现了PagedAttention以提高内存效率，并使用自定义Triton内核以提升性能。

### How does Mini-Infer compare to vLLM? | Mini-Infer与vLLM相比如何？

**Similarities | 相似之处:**

- Both use PagedAttention for KV cache management
- Both implement continuous batching
- Similar architecture design

**Differences | 不同之处:**

- Mini-Infer: Focused on simplicity and learning (目标：简洁性和学习)
- vLLM: Production-ready with more features (生产就绪，功能更多)
- Mini-Infer targets 85-90% of vLLM's performance (目标性能为vLLM的85-90%)

### Is Mini-Infer production-ready? | Mini-Infer可以用于生产吗？

Not yet. Mini-Infer is currently in **alpha** (v0.1.x). It's designed for:

- Learning about LLM inference optimization
- Research and experimentation
- Prototyping

For production use, consider [vLLM](https://github.com/vllm-project/vllm) or [TGI](https://github.com/huggingface/text-generation-inference).

目前还不可以。Mini-Infer目前处于**alpha**阶段（v0.1.x）。它设计用于：

- 学习LLM推理优化
- 研究和实验
- 原型开发

对于生产使用，请考虑 [vLLM](https://github.com/vllm-project/vllm) 或 [TGI](https://github.com/huggingface/text-generation-inference)。

---

## Installation & Setup | 安装和设置

### What GPU do I need? | 我需要什么GPU？

**Minimum | 最低要求:**

- NVIDIA GPU with compute capability 7.0+
- Examples: V100, T4, RTX 2080 Ti

**Recommended | 推荐:**

- A100, A6000, RTX 4090
- 40GB+ VRAM for larger models

### Can I run Mini-Infer on CPU? | 可以在CPU上运行Mini-Infer吗？

No. Mini-Infer requires CUDA-capable NVIDIA GPUs because:

- Triton kernels are GPU-only
- PagedAttention optimization targets GPUs

不可以。Mini-Infer需要支持CUDA的NVIDIA GPU，因为：

- Triton内核仅支持GPU
- PagedAttention优化针对GPU

### Can I use AMD GPUs? | 可以使用AMD GPU吗？

Currently, no. Mini-Infer uses:

- CUDA (NVIDIA-specific)
- Triton (primarily CUDA-focused)

Future support for ROCm (AMD) may be considered.

目前不可以。Mini-Infer使用：

- CUDA（NVIDIA专用）
- Triton（主要针对CUDA）

未来可能考虑支持ROCm（AMD）。

### What Python version is required? | 需要什么Python版本？

Python **3.10 or 3.11** is required.

- Python 3.9: Not supported (缺少某些类型提示功能)
- Python 3.12: Not yet tested (Triton兼容性未验证)

需要Python **3.10或3.11**。

---

## Performance | 性能

### How fast is Mini-Infer? | Mini-Infer有多快？

**Target Performance Metrics | 目标性能指标:**

| Component | Baseline | Mini-Infer | Speedup |
|-----------|----------|------------|---------|
| RMSNorm | PyTorch | Triton | 5-8x |
| RoPE | PyTorch | Triton | 6-8x |
| Memory Util | 40% | 85%+ | 2x+ |
| Throughput | Static | Continuous | 2-3x |

Actual performance varies by model, batch size, and hardware.

实际性能因模型、批量大小和硬件而异。

### Why is my inference slow? | 为什么我的推理很慢？

**Common Causes | 常见原因:**

1. **Small batch size | 批量太小**
   - GPUs are under-utilized with batch_size < 8
   - Try increasing `max_num_seqs` in config

2. **Memory bottleneck | 内存瓶颈**
   - Check `gpu_memory_utilization` is 0.85-0.95
   - Ensure enough VRAM for KV cache

3. **Not using Triton kernels | 未使用Triton内核**
   - Verify Triton is installed correctly
   - Check kernel compilation logs

4. **Model loading time | 模型加载时间**
   - First inference is slow (model loading)
   - Subsequent inferences should be faster

### How do I benchmark Mini-Infer? | 如何对Mini-Infer进行基准测试？

```bash
# Install benchmark dependencies
pip install -e ".[benchmark]"

# Run benchmarks (coming soon)
python benchmarks/run_benchmark.py \
    --model meta-llama/Llama-2-7b-hf \
    --batch-sizes 1,8,16,32 \
    --input-len 128 \
    --output-len 128
```

---

## Models | 模型

### What models are supported? | 支持哪些模型？

Currently targeting **Llama-style** architectures:

- Llama 2 (7B, 13B, 70B)
- Llama 3
- Mistral
- Other Llama-based models

Support for more architectures (GPT, BLOOM, etc.) planned.

当前针对**Llama风格**架构：

- Llama 2 (7B, 13B, 70B)
- Llama 3
- Mistral
- 其他基于Llama的模型

计划支持更多架构（GPT、BLOOM等）。

### Can I use custom/fine-tuned models? | 可以使用自定义/微调模型吗？

Yes, as long as they follow the Llama architecture. Load from:

- HuggingFace Hub
- Local path

可以，只要它们遵循Llama架构。可以从以下位置加载：

- HuggingFace Hub
- 本地路径

```python
config = EngineConfig(
    model="path/to/your/model",
    trust_remote_code=True  # If needed
)
```

### How much VRAM does a 7B model need? | 7B模型需要多少VRAM？

**Approximate VRAM usage | 大致VRAM使用:**

| Model Size | FP16 Weights | + KV Cache | Total |
|-----------|--------------|------------|-------|
| 7B | ~14GB | ~6GB | **~20GB** |
| 13B | ~26GB | ~10GB | **~36GB** |
| 70B | ~140GB | ~30GB | **~170GB** |

*KV cache size depends on batch size and sequence length*

*KV缓存大小取决于批量大小和序列长度*

---

## Features | 功能

### Does Mini-Infer support quantization? | Mini-Infer支持量化吗？

Not yet in v0.1. Planned for future releases:

- INT8 quantization
- INT4/GPTQ support
- AWQ support

v0.1版本中还不支持。计划在未来版本中支持：

- INT8量化
- INT4/GPTQ支持
- AWQ支持

### Does it support multi-GPU inference? | 支持多GPU推理吗？

Not in v0.1. Planned features:

- Tensor parallelism
- Pipeline parallelism

v0.1版本中不支持。计划功能：

- 张量并行
- 流水线并行

### Can I use it for training? | 可以用于训练吗？

No. Mini-Infer is **inference-only**. For training, use:

- PyTorch native
- DeepSpeed
- Megatron-LM

不可以。Mini-Infer**仅用于推理**。对于训练，请使用：

- PyTorch原生
- DeepSpeed
- Megatron-LM

---

## Troubleshooting | 故障排除

### "CUDA out of memory" error | CUDA内存不足错误

**Solutions | 解决方案:**

1. Reduce batch size | 减少批量大小:

   ```python
   config = EngineConfig(max_num_seqs=16)  # Instead of 64
   ```

2. Lower memory utilization | 降低内存利用率:

   ```python
   config = EngineConfig(gpu_memory_utilization=0.8)
   ```

3. Use smaller model | 使用更小的模型:
   - Try 7B instead of 13B

4. Enable CPU offloading (future) | 启用CPU卸载（未来）

### "Triton kernel compilation failed" | Triton内核编译失败

**Check | 检查:**

1. CUDA toolkit installed | CUDA工具包已安装:

   ```bash
   nvcc --version
   ```

2. Environment variables set | 环境变量已设置:

   ```bash
   export PATH=/usr/local/cuda/bin:$PATH
   export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
   ```

3. Triton version compatible | Triton版本兼容:

   ```bash
   pip install triton==2.1.0
   ```

### Inference is very slow | 推理非常慢

**Debug steps | 调试步骤:**

1. Profile to find bottleneck | 分析找出瓶颈:

   ```python
   # Add profiling (coming soon)
   ```

2. Check Triton kernels are compiling | 检查Triton内核是否编译:

   ```bash
   export TRITON_DEBUG=1
   ```

3. Verify GPU utilization | 验证GPU利用率:

   ```bash
   nvidia-smi -l 1
   ```

---

## Development | 开发

### How can I contribute? | 如何贡献？

See [CONTRIBUTING.md](file:///h:/就业/mini-infer/CONTRIBUTING.md) for:

- Code style guidelines
- Development setup
- Pull request process

参见 [CONTRIBUTING.md](file:///h:/就业/mini-infer/CONTRIBUTING.md) 了解：

- 代码风格指南
- 开发环境设置
- Pull request流程

### Where should I report bugs? | 应该在哪里报告bug？

Use [GitHub Issues](https://github.com/psmarter/mini-infer/issues):

- Choose "Bug Report" template
- Provide environment details
- Include error logs

使用 [GitHub Issues](https://github.com/psmarter/mini-infer/issues):

- 选择"Bug Report"模板
- 提供环境详细信息
- 包含错误日志

### How do I request features? | 如何请求功能？

Use [GitHub Issues](https://github.com/psmarter/mini-infer/issues):

- Choose "Feature Request" template
- Describe use case
- Explain why it's useful

使用 [GitHub Issues](https://github.com/psmarter/mini-infer/issues):

- 选择"Feature Request"模板
- 描述用例
- 解释为什么有用

---

## Comparison with Other Tools | 与其他工具的比较

### Mini-Infer vs. vLLM

| Feature | Mini-Infer | vLLM |
|---------|-----------|------|
| **Purpose** | Learning/Research | Production |
| **Performance** | 85-90% of vLLM | Baseline |
| **Code Complexity** | Simpler | More complex |
| **Features** | Core only | Comprehensive |
| **Stability** | Alpha | Stable |

### Mini-Infer vs. Transformers

| Feature | Mini-Infer | Transformers |
|---------|-----------|--------------|
| **Speed** | Much faster | Baseline |
| **Memory** | Efficient (PagedAttention) | Standard |
| **Batching** | Continuous | Static |
| **Use Case** | Inference | Training + Inference |

### Mini-Infer vs. TGI (Text Generation Inference)

| Feature | Mini-Infer | TGI |
|---------|-----------|-----|
| **Scope** | Learning project | Production server |
| **Deployment** | Library | REST API server |
| **Models** | Llama-style | Many architectures |
| **Maturity** | Alpha | Production-ready |

---

## License & Usage | 许可证和使用

### What license does Mini-Infer use? | Mini-Infer使用什么许可证？

MIT License - very permissive:

- ✅ Commercial use allowed
- ✅ Modification allowed
- ✅ Distribution allowed
- ✅ Private use allowed

MIT许可证 - 非常宽松：

- ✅ 允许商业使用
- ✅ 允许修改
- ✅ 允许分发
- ✅ 允许私人使用

See [LICENSE](file:///h:/就业/mini-infer/LICENSE) for details.

### Can I use it in my company? | 可以在公司使用吗？

Yes, but with caution:

- It's still in **alpha** (unstable)
- Recommended for research/prototyping
- Not recommended for production yet

可以，但需谨慎：

- 仍处于**alpha**阶段（不稳定）
- 建议用于研究/原型开发
- 暂不建议用于生产

---

## Getting More Help | 获取更多帮助

### Documentation | 文档

- [README](file:///h:/就业/mini-infer/README.md) - Overview and quick start
- [Installation](file:///h:/就业/mini-infer/docs/installation.md) - Detailed installation guide
- [Architecture](file:///h:/就业/mini-infer/docs/architecture.md) - System design
- [API Reference](file:///h:/就业/mini-infer/docs/api_reference.md) - API documentation

### Community | 社区

- [GitHub Issues](https://github.com/psmarter/mini-infer/issues) - Bug reports, features
- [GitHub Discussions](https://github.com/psmarter/mini-infer/discussions) - (Coming soon) Questions, ideas

### Contact | 联系方式

- Email: <smarter.shh1104@gmail.com>
- GitHub: [@psmarter](https://github.com/psmarter)

---

**Don't see your question? | 没找到你的问题？**

[Open an issue](https://github.com/psmarter/mini-infer/issues/new/choose) or contribute to this FAQ!

[提交issue](https://github.com/psmarter/mini-infer/issues/new/choose) 或为此FAQ做贡献！
