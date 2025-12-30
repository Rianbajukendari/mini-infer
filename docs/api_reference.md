# API Reference | API参考

> [!NOTE]
> This API reference is for the planned v0.1.0 release. Implementation is in progress.
>
> 此API参考适用于计划中的v0.1.0版本。实现正在进行中。

---

## Table of Contents | 目录

- [Core Classes](#core-classes--核心类)
  - [LLMEngine](#llmengine)
  - [EngineConfig](#engineconfig)
- [Scheduler](#scheduler--调度器)
- [Memory Management](#memory-management--内存管理)
- [Kernels](#kernels--内核)
- [Utilities](#utilities--工具)

---

## Core Classes | 核心类

### LLMEngine

The main inference engine for running LLM models.

用于运行LLM模型的主推理引擎。

#### Constructor

```python
from mini_infer import LLMEngine
from mini_infer.config import EngineConfig

config = EngineConfig(
    model="meta-llama/Llama-2-7b-hf",
    max_num_seqs=64,
    block_size=16
)
engine = LLMEngine(config)
```

**Parameters | 参数:**

- `config` (EngineConfig): Engine configuration object | 引擎配置对象

#### Methods

##### `generate()`

Generate text from prompts.

从提示生成文本。

```python
outputs = engine.generate(
    prompts=["Hello, how are you?"],
    max_tokens=100,
    temperature=0.8,
    top_p=0.95
)
```

**Parameters | 参数:**

- `prompts` (List[str]): Input prompts | 输入提示
- `max_tokens` (int, optional): Maximum tokens to generate | 生成的最大token数. Default: 100
- `temperature` (float, optional): Sampling temperature | 采样温度. Default: 1.0
- `top_p` (float, optional): Nucleus sampling parameter | 核采样参数. Default: 1.0
- `top_k` (int, optional): Top-k sampling parameter | Top-k采样参数. Default: -1 (disabled)

**Returns | 返回:**

- `List[GenerateOutput]`: Generation results | 生成结果

##### `add_request()`

Add a single request to the engine queue.

向引擎队列添加单个请求。

```python
request_id = engine.add_request(
    prompt="Write a poem",
    max_tokens=50,
    sampling_params=SamplingParams(temperature=0.9)
)
```

**Parameters | 参数:**

- `prompt` (str): Input prompt | 输入提示
- `max_tokens` (int): Maximum tokens | 最大token数
- `sampling_params` (SamplingParams, optional): Sampling configuration | 采样配置

**Returns | 返回:**

- `str`: Request ID | 请求ID

##### `get_output()`

Retrieve output for a completed request.

检索已完成请求的输出。

```python
output = engine.get_output(request_id)
```

**Parameters | 参数:**

- `request_id` (str): Request identifier | 请求标识符

**Returns | 返回:**

- `GenerateOutput | None`: Output if ready, None otherwise | 如果就绪则返回输出，否则返回None

---

### EngineConfig

Configuration for the LLMEngine.

LLMEngine的配置。

```python
from mini_infer.config import EngineConfig

config = EngineConfig(
    model="meta-llama/Llama-2-7b-hf",
    tokenizer="meta-llama/Llama-2-7b-hf",
    max_num_seqs=64,
    max_model_len=2048,
    block_size=16,
    gpu_memory_utilization=0.9,
    dtype="float16"
)
```

**Parameters | 参数:**

- `model` (str): HuggingFace model name or path | HuggingFace模型名称或路径
- `tokenizer` (str, optional): Tokenizer name/path | 分词器名称/路径. Defaults to model
- `max_num_seqs` (int): Maximum concurrent sequences | 最大并发序列数. Default: 256
- `max_model_len` (int, optional): Maximum sequence length | 最大序列长度. Default: from model config
- `block_size` (int): KV cache block size in tokens | KV缓存块大小（token数）. Default: 16
- `gpu_memory_utilization` (float): GPU memory utilization fraction | GPU内存利用率. Default: 0.9
- `dtype` (str): Data type ("float16", "bfloat16", "float32") | 数据类型. Default: "float16"
- `trust_remote_code` (bool): Trust remote code in model | 信任模型中的远程代码. Default: False

---

## Scheduler | 调度器

### Scheduler

Continuous batching scheduler for request management.

用于请求管理的连续批处理调度器。

```python
from mini_infer.scheduler import Scheduler

scheduler = Scheduler(
    max_num_seqs=64,
    max_model_len=2048,
    block_size=16
)
```

#### Methods

##### `schedule()`

Schedule next batch of requests.

调度下一批请求。

```python
scheduled_seqs = scheduler.schedule()
```

**Returns | 返回:**

- `SchedulerOutputs`: Scheduled sequences and metadata | 调度的序列和元数据

---

## Memory Management | 内存管理

### BlockManager

Manages PagedAttention memory blocks.

管理PagedAttention内存块。

```python
from mini_infer.memory import BlockManager

block_manager = BlockManager(
    block_size=16,
    num_gpu_blocks=1024,
    num_cpu_blocks=256
)
```

**Parameters | 参数:**

- `block_size` (int): Tokens per block | 每块的token数
- `num_gpu_blocks` (int): Total GPU blocks | GPU块总数
- `num_cpu_blocks` (int): Total CPU blocks for swapping | 用于交换的CPU块总数

#### Methods

##### `allocate()`

Allocate memory blocks for a sequence.

为序列分配内存块。

```python
blocks = block_manager.allocate(num_blocks=4)
```

**Parameters | 参数:**

- `num_blocks` (int): Number of blocks needed | 需要的块数

**Returns | 返回:**

- `List[int]`: Allocated block IDs | 分配的块ID

##### `free()`

Free memory blocks.

释放内存块。

```python
block_manager.free(blocks)
```

**Parameters | 参数:**

- `blocks` (List[int]): Block IDs to free | 要释放的块ID

##### `can_allocate()`

Check if blocks can be allocated.

检查是否可以分配块。

```python
can_allocate = block_manager.can_allocate(num_blocks=4)
```

**Returns | 返回:**

- `bool`: True if allocation possible | 如果可以分配则返回True

---

## Kernels | 内核

### RMSNorm

RMSNorm kernel with Triton optimization.

使用Triton优化的RMSNorm内核。

```python
from mini_infer.kernels import rmsnorm

output = rmsnorm(
    x=input_tensor,
    weight=weight_tensor,
    eps=1e-6
)
```

**Parameters | 参数:**

- `x` (Tensor): Input tensor [batch, seq_len, hidden_size] | 输入张量
- `weight` (Tensor): Normalization weights [hidden_size] | 归一化权重
- `eps` (float): Epsilon for numerical stability | 数值稳定性的epsilon

**Returns | 返回:**

- `Tensor`: Normalized output | 归一化输出

**Performance | 性能:**

- Target: 5-8x faster than PyTorch | 目标：比PyTorch快5-8倍

---

### RoPE

Rotary Position Embedding kernel.

旋转位置嵌入内核。

```python
from mini_infer.kernels import apply_rotary_emb

output_q, output_k = apply_rotary_emb(
    q=query_tensor,
    k=key_tensor,
    cos=cos_cached,
    sin=sin_cached,
    position_ids=positions
)
```

**Parameters | 参数:**

- `q` (Tensor): Query tensor | 查询张量
- `k` (Tensor): Key tensor | 键张量
- `cos` (Tensor): Cosine values | 余弦值
- `sin` (Tensor): Sine values | 正弦值
- `position_ids` (Tensor): Position indices | 位置索引

**Returns | 返回:**

- `Tuple[Tensor, Tensor]`: Rotated query and key | 旋转后的查询和键

**Performance | 性能:**

- Target: 6-8x faster than PyTorch | 目标：比PyTorch快6-8倍

---

### PagedAttention

Attention kernel with paged KV cache.

具有分页KV缓存的注意力内核。

```python
from mini_infer.kernels import paged_attention

output = paged_attention(
    query=q,
    key_cache=k_cache,
    value_cache=v_cache,
    block_tables=block_tables,
    context_lens=context_lengths
)
```

**Parameters | 参数:**

- `query` (Tensor): Query states | 查询状态
- `key_cache` (Tensor): Paged key cache | 分页键缓存
- `value_cache` (Tensor): Paged value cache | 分页值缓存
- `block_tables` (Tensor): Block mapping table | 块映射表
- `context_lens` (Tensor): Context lengths | 上下文长度

**Returns | 返回:**

- `Tensor`: Attention output | 注意力输出

---

## Utilities | 工具

### SamplingParams

Parameters for text generation sampling.

文本生成采样的参数。

```python
from mini_infer.sampling import SamplingParams

params = SamplingParams(
    temperature=0.8,
    top_p=0.95,
    top_k=50,
    max_tokens=100
)
```

**Parameters | 参数:**

- `temperature` (float): Sampling temperature | 采样温度. Default: 1.0
- `top_p` (float): Nucleus sampling threshold | 核采样阈值. Default: 1.0
- `top_k` (int): Top-k sampling limit | Top-k采样限制. Default: -1
- `max_tokens` (int): Maximum tokens to generate | 生成的最大token数. Default: 16

---

### GenerateOutput

Output from text generation.

文本生成的输出。

**Attributes | 属性:**

- `text` (str): Generated text | 生成的文本
- `token_ids` (List[int]): Generated token IDs | 生成的token ID
- `finish_reason` (str): Completion reason ("stop", "length") | 完成原因
- `cumulative_logprob` (float): Cumulative log probability | 累积对数概率

---

## Example Usage | 使用示例

### Basic Generation | 基础生成

```python
from mini_infer import LLMEngine
from mini_infer.config import EngineConfig

# Initialize
config = EngineConfig(model="meta-llama/Llama-2-7b-hf")
engine = LLMEngine(config)

# Generate
outputs = engine.generate(
    prompts=["Explain quantum computing in simple terms."],
    max_tokens=200
)

print(outputs[0].text)
```

### Batch Generation | 批量生成

```python
prompts = [
    "Write a haiku about programming",
    "Explain recursion",
    "What is machine learning?"
]

outputs = engine.generate(
    prompts=prompts,
    max_tokens=100,
    temperature=0.7
)

for i, output in enumerate(outputs):
    print(f"Prompt {i}: {output.text}\n")
```

### Async Request Handling | 异步请求处理

```python
# Add requests
req_ids = []
for prompt in prompts:
    req_id = engine.add_request(prompt, max_tokens=50)
    req_ids.append(req_id)

# Poll for results
while req_ids:
    for req_id in req_ids[:]:
        output = engine.get_output(req_id)
        if output:
            print(f"{req_id}: {output.text}")
            req_ids.remove(req_id)
```

---

## Error Handling | 错误处理

```python
from mini_infer.exceptions import (
    OutOfMemoryError,
    InvalidRequestError,
    ModelNotFoundError
)

try:
    engine = LLMEngine(config)
    outputs = engine.generate(prompts)
except OutOfMemoryError:
    print("Not enough GPU memory")
except InvalidRequestError as e:
    print(f"Invalid request: {e}")
except ModelNotFoundError:
    print("Model not found")
```

---

## Type Hints | 类型提示

Mini-Infer is fully typed. Import types for better IDE support:

Mini-Infer完全支持类型提示。导入类型以获得更好的IDE支持：

```python
from mini_infer.typing import (
    TokenIds,
    BlockTable,
    SequenceMetadata
)
```

---

> [!TIP]
> For more examples, see the [examples/](file:///h:/就业/mini-infer/examples) directory.
>
> 更多示例请参见 [examples/](file:///h:/就业/mini-infer/examples) 目录。
