# Examples | 示例

This directory contains usage examples for Mini-Infer.

此目录包含Mini-Infer的使用示例。

---

## Available Examples | 可用示例

### [quickstart.py](file:///h:/就业/mini-infer/examples/quickstart.py)

Basic usage example showing how to initialize the engine and generate text.

展示如何初始化引擎和生成文本的基础用法示例。

**Status | 状态:** 🚧 Preview - Implementation in progress

---

## Running Examples | 运行示例

> [!NOTE]
> Examples are currently **preview versions** showing the intended API.
> Full implementation coming soon as core features are completed.
>
> 示例目前是**预览版本**，展示预期的API。
> 完整实现即将推出，待核心功能完成后。

### Prerequisites | 前置条件

1. Install Mini-Infer:

   ```bash
   pip install -e .
   ```

2. Ensure CUDA is available:

   ```python
   python -c "import torch; print(torch.cuda.is_available())"
   ```

### Run Quickstart | 运行快速开始

```bash
python examples/quickstart.py
```

---

## Planned Examples | 计划中的示例

### Basic Inference | 基础推理

```python
# examples/basic_inference.py (coming soon)
from mini_infer import LLMEngine
from mini_infer.config import EngineConfig

config = EngineConfig(model="meta-llama/Llama-2-7b-hf")
engine = LLMEngine(config)

outputs = engine.generate(
    prompts=["Explain machine learning in simple terms."],
    max_tokens=200
)
print(outputs[0].text)
```

### Batch Processing | 批量处理

```python
# examples/batch_processing.py (coming soon)
prompts = [
    "Write a haiku about coding",
    "Explain recursion",
    "What is a transformer model?"
]

outputs = engine.generate(
    prompts=prompts,
    max_tokens=100,
    temperature=0.7
)

for i, output in enumerate(outputs):
    print(f"\n=== Prompt {i+1} ===")
    print(output.text)
```

### Streaming Generation | 流式生成

```python
# examples/streaming.py (coming soon)
for token in engine.generate_stream(
    prompt="Write a short story",
    max_tokens=500
):
    print(token, end='', flush=True)
```

### Custom Sampling | 自定义采样

```python
# examples/custom_sampling.py (coming soon)
from mini_infer.sampling import SamplingParams

# Creative sampling
creative_params = SamplingParams(
    temperature=0.9,
    top_p=0.95,
    top_k=50
)

# Deterministic sampling
deterministic_params = SamplingParams(
    temperature=0.0,  # Greedy
)

outputs_creative = engine.generate(
    prompts=["Write a creative story"],
    sampling_params=creative_params
)

outputs_deterministic = engine.generate(
    prompts=["Summarize: ..."],
    sampling_params=deterministic_params
)
```

### Benchmarking | 基准测试

```python
# examples/benchmark.py (coming soon)
import time

prompts = ["Test prompt"] * 32  # Batch of 32

start = time.time()
outputs = engine.generate(prompts, max_tokens=100)
end = time.time()

throughput = (32 * 100) / (end - start)
print(f"Throughput: {throughput:.2f} tokens/sec")
```

---

## Example Output | 示例输出

### Expected Output Format | 预期输出格式

```python
# GenerateOutput object
output = outputs[0]

print(f"Generated text: {output.text}")
print(f"Token IDs: {output.token_ids}")
print(f"Finish reason: {output.finish_reason}")  # 'stop' or 'length'
print(f"Log probability: {output.cumulative_logprob}")
```

---

## Tips for Examples | 示例提示

### Memory Management | 内存管理

```python
# For large batches, monitor memory
config = EngineConfig(
    model="meta-llama/Llama-2-7b-hf",
    max_num_seqs=32,  # Reduce if OOM
    gpu_memory_utilization=0.85
)
```

### Model Selection | 模型选择

```python
# Start with smaller models for testing
models = {
    "small": "meta-llama/Llama-2-7b-hf",  # ~14GB VRAM
    "medium": "meta-llama/Llama-2-13b-hf",  # ~26GB VRAM
    "large": "meta-llama/Llama-2-70b-hf",  # ~140GB VRAM (multi-GPU)
}
```

### Error Handling | 错误处理

```python
from mini_infer.exceptions import OutOfMemoryError, ModelNotFoundError

try:
    engine = LLMEngine(config)
    outputs = engine.generate(prompts)
except OutOfMemoryError:
    print("Reduce batch size or use smaller model")
except ModelNotFoundError:
    print("Check model name/path")
```

---

## Contributing Examples | 贡献示例

Have a useful example? Contribute it!

有有用的示例吗？贡献它！

1. Create a new `.py` file in `examples/`
2. Add clear comments and docstrings
3. Update this README
4. Submit a pull request

See [CONTRIBUTING.md](file:///h:/就业/mini-infer/CONTRIBUTING.md) for guidelines.

---

## Getting Help | 获取帮助

- [API Reference](file:///h:/就业/mini-infer/docs/api_reference.md) - Detailed API documentation
- [FAQ](file:///h:/就业/mini-infer/docs/faq.md) - Common questions
- [GitHub Issues](https://github.com/psmarter/mini-infer/issues) - Bug reports and questions
