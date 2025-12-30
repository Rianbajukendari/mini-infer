# 快速修复指南 | Quick Fix Guide

## ⚠️ 当前问题 | Current Issue

GitHub Actions "Code Quality" workflow 失败  
**原因**: Black代码格式检查失败

---

## ✅ 3分钟快速修复 | Quick Fix (3 minutes)

### 步骤 1: 格式化代码

```bash
# 进入项目目录
cd "h:/就业/mini-infer"

# 安装black（如果还没安装）
pip install black

# 运行格式化
black .

# 提交修复
git add .
git commit -m "style: format code with black"
git push origin main
```

### 步骤 2: 验证修复

1. 访问 <https://github.com/psmarter/mini-infer/actions>
2. 等待2-3分钟
3. 查看最新的"Code Quality" workflow
4. 应该显示 ✅ 通过

---

## 🎯 预期结果 | Expected Result

修复后，两个workflows都应该通过：

- ✅ Tests: PASS
- ✅ Code Quality: PASS

---

## 💡 如果遇到问题 | If You Encounter Issues

### 问题1: black命令不存在

**解决方案**:

```bash
pip install black
```

### 问题2: 不确定修改了什么

**查看修改**:

```bash
git diff
```

Black可能会修改:

- 行长度（超过100字符会换行）
- 引号统一（全部用双引号）
- 空格和缩进
- import顺序

这些都是**安全的格式化修改**，不会影响代码逻辑！

---

## ✅ 完成后

配置将达到100分！然后可以开始Week 2的开发工作。

---

**记住**: 格式化是为了代码可读性和一致性，不会改变功能！
