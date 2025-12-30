# Contributing to Mini-Infer

欢迎贡献! | Welcome to contribute!

## 如何贡献 | How to Contribute

### 报告Bug | Report Bugs

请使用GitHub Issues报告bug，并包含：
Please use GitHub Issues to report bugs, include:

- 详细的错误描述 | Detailed error description
- 复现步骤 | Steps to reproduce
- 系统环境 | System environment

### 提交代码 | Submit Code

1. Fork 本仓库 | Fork this repository
2. 创建特性分支 | Create feature branch

   ```bash
   git checkout -b feature/AmazingFeature
   ```

3. 提交更改 | Commit changes

   ```bash
   git commit -m 'feat: Add some AmazingFeature'
   ```

4. 推送到分支 | Push to branch

   ```bash
   git push origin feature/AmazingFeature
   ```

5. 开启Pull Request

### 代码规范 | Code Standards

```bash
# 格式化 | Format
black mini_infer/ tests/

# Lint检查 | Lint
flake8 mini_infer/ tests/

# 测试 | Test
pytest tests/
```

### Commit消息规范 | Commit Message Convention

```
feat: 新功能 | New feature
fix: 修复bug | Bug fix
docs: 文档更新 | Documentation update
test: 测试相关 | Test related
refactor: 代码重构 | Code refactoring
perf: 性能优化 | Performance optimization
```

## 开发流程 | Development Workflow

1. 先创建Issue讨论 | Create Issue first
2. 获得批准后开始开发 | Start development after approval
3. 编写测试用例 | Write test cases
4. 确保CI通过 | Ensure CI passes
5. 提交PR等待review | Submit PR for review

感谢你的贡献! | Thank you for your contribution!
