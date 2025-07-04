# LLM_RAG

基于 LangChain 的智能问答系统，结合向量数据库和大语言模型实现知识库增强对话。

## 功能特性

- 📚 **文档处理**: 支持 PDF 和 Markdown 文件的加载与处理
- 🔍 **向量检索**: 使用 ChromaDB 构建向量数据库，实现语义相似度搜索
- 🤖 **多模型支持**: 集成硅基流动 API 和智谱 AI 嵌入模型
- 💬 **智能对话**: 基于检索增强生成 (RAG) 的问答系统
- 🎯 **相关推荐**: 根据对话上下文自动生成相关问题建议

## 快速开始

### 环境配置

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置环境变量：
```bash
# 创建 .env 文件
SILICON_FLOW=your_silicon_flow_api_key
ZHIPUAI_API_KEY=your_zhipuai_api_key
```

### 使用步骤

1. **构建向量数据库**：
```bash
python build_vec_db.py
```

2. **启动问答系统**：
```bash
python demo.py
```

## 项目结构

```
LLM_RAG/
├── build_vec_db.py     # 构建向量数据库
├── demo.py             # 主程序：交互式问答系统
├── data_proc.py        # 数据预处理
├── ds_llm.py           # 自定义 LLM 封装
├── zhipuai_embedding.py # 智谱 AI 嵌入模型封装
├── requirements.txt    # 项目依赖
├── test/               # 测试文件
└── data_base/          # 数据存储目录
```

## 核心组件

- **文档加载器**: 支持 PDF (PyMuPDF) 和 Markdown 文件
- **文本分割**: 使用递归字符分割器，支持自定义 chunk 大小
- **向量化**: 智谱 AI embedding-2 模型
- **向量存储**: ChromaDB 持久化存储
- **大语言模型**: 硅基流动 DeepSeek-V2.5 模型

## 后期计划

### 🚀 功能增强
- [ ] 支持更多文件格式 (Word, Excel, PPT)
- [ ] 添加网页爬虫功能，支持在线文档处理
- [ ] 实现多轮对话记忆机制
- [ ] 添加文档摘要和关键词提取功能
- [ ] 支持图片和表格内容理解

### 🎨 用户体验
- [ ] 开发 Web UI 界面 (Gradio/Streamlit)
- [ ] 添加语音问答功能
- [ ] 实现实时流式回答
- [ ] 支持多语言问答
- [ ] 添加问答历史记录和导出功能

### 🔧 技术优化
- [ ] 支持更多向量数据库 (Pinecone, Weaviate)
- [ ] 集成更多 LLM 模型 (GPT-4, Claude, 本地模型)
- [ ] 实现混合检索 (关键词 + 向量检索)
- [ ] 添加检索结果重排序
- [ ] 优化文档分块策略

### 🏗️ 架构升级
- [ ] 微服务架构重构
- [ ] 添加 RESTful API 接口
- [ ] 实现分布式部署支持
- [ ] 添加监控和日志系统
- [ ] 支持用户权限管理

### 📊 分析工具
- [ ] 问答质量评估系统
- [ ] 用户行为分析
- [ ] 知识库使用统计
- [ ] 性能监控面板

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

本项目采用 MIT 许可证。
