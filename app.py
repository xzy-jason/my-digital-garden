#!/usr/bin/env python3
"""
我的数字花园 - Flask 后端
提供访客计数和留言板 API
"""

import sqlite3
import os
from flask import Flask, jsonify, request, send_from_directory
from datetime import datetime

app = Flask(__name__, static_folder='.')
DB_PATH = os.path.join(os.path.dirname(__file__), 'garden.db')

def init_db():
    """初始化数据库"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 访客计数表
    c.execute('''CREATE TABLE IF NOT EXISTS visitors (
        id INTEGER PRIMARY KEY,
        count INTEGER DEFAULT 0,
        last_visit TEXT
    )''')
    
    # 留言表
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        message TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # 初始化访客计数
    c.execute('SELECT count FROM visitors WHERE id = 1')
    row = c.fetchone()
    if row is None:
        c.execute('INSERT INTO visitors (id, count) VALUES (1, 0)')
    
    conn.commit()
    conn.close()

def get_visitor_count():
    """获取访客计数"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT count FROM visitors WHERE id = 1')
    row = c.fetchone()
    conn.close()
    return row[0] if row else 0

def increment_visitor():
    """增加访客计数"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE visitors SET count = count + 1, last_visit = ? WHERE id = 1', 
              (datetime.now().isoformat(),))
    conn.commit()
    conn.close()

def get_messages(limit=20):
    """获取留言列表"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT name, message, created_at FROM messages ORDER BY id DESC LIMIT ?', 
              (limit,))
    rows = c.fetchall()
    conn.close()
    return [{'name': r[0], 'message': r[1], 'created_at': r[2]} for r in rows]

def add_message(name, message):
    """添加留言"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO messages (name, message) VALUES (?, ?)', 
              (name, message))
    conn.commit()
    conn.close()

# API 路由
@app.route('/api/visitor-count', methods=['GET'])
def api_visitor_count():
    """获取访客计数"""
    count = get_visitor_count()
    increment_visitor()  # 每次访问都增加计数
    return jsonify({'count': count})

@app.route('/api/messages', methods=['GET'])
def api_get_messages():
    """获取留言列表"""
    messages = get_messages()
    return jsonify(messages)

@app.route('/api/messages', methods=['POST'])
def api_add_message():
    """添加留言"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    name = data.get('name', '').strip()
    message = data.get('message', '').strip()
    
    if not name or not message:
        return jsonify({'error': 'Name and message are required'}), 400
    
    add_message(name, message)
    return jsonify({'success': True})

@app.route('/')
def index():
    """主页"""
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    init_db()
    print("🌻 我的数字花园后端服务启动中...")
    print("访问地址: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)