# 贡献指南

感谢你对三豆-AI技能库的兴趣！

## 如何贡献

### 1. 报告问题

如果你发现了bug或有改进建议，请创建一个[Issue](https://github.com/zimuge-doudou/san-dou-ai-skills/issues)。

### 2. 提交代码

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建一个 Pull Request

### 3. 添加新技能

如果你想添加一个新的技能，请遵循以下步骤：

1. 在 `skills/` 目录下创建新目录
2. 创建 `SKILL.md` 描述技能
3. 创建实现文件
4. 添加测试
5. 更新文档

## 代码规范

- 使用Python 3.8+
- 遵循PEP 8规范
- 添加类型提示
- 编写文档字符串
- 添加单元测试

## 安全要求

- **绝对禁止**硬编码敏感信息（API密钥、密码、Token等）
- 所有敏感信息必须使用环境变量
- 上传前必须进行安全扫描

## 测试要求

- 所有新功能必须有单元测试
- 测试覆盖率 > 80%
- 通过CI/CD检查

## 文档要求

- 更新README.md
- 添加使用示例
- 更新API文档

## 行为准则

- 尊重所有贡献者
- 接受建设性批评
- 专注于对社区最有利的事情
- 对其他社区成员表示同理心

感谢你的贡献！
