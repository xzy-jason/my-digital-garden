# 🌻 我的数字花园

一个植物主题的个人展示网站，包含前端页面和 Flask 后端。

## 功能特性

- 🌱 个人介绍区
- 🌷 技能花园（植物进度条展示技能等级）
- 🌿 成长时间线
- 🍀 爱好卡片展示
- 🌸 留言板（后端 API + SQLite 数据库）
- 📊 访客计数

## 技术栈

- **前端：** HTML + CSS + JavaScript（无框架）
- **后端：** Python Flask
- **数据库：** SQLite

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/xzy-jason/my-digital-garden.git
cd my-digital-garden
```

### 2. 安装依赖

```bash
pip install flask
```

### 3. 启动服务

```bash
python app.py
```

然后访问 http://localhost

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | / | 主页 |
| GET | /api/visitor-count | 获取访客计数 |
| GET | /api/messages | 获取留言列表 |
| POST | /api/messages | 提交留言 |

### 提交留言示例

```bash
curl -X POST http://localhost/api/messages \
  -H "Content-Type: application/json" \
  -d '{"name":"你的名字","message":"留言内容"}'
```

## 项目结构

```
my-digital-garden/
├── index.html    # 前端页面
├── app.py        # Flask 后端
├── garden.db     # SQLite 数据库（自动创建）
└── README.md     # 本文件
```

## 截图

![首页](screenshot.png)

---
🌱 用心浇灌每一行代码