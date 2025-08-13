import json
from threading import Lock
import threading

def write_to_jsonl(filename, data):
    print("write_to_jsonl")
    lock = threading.Lock()  # 创建一个锁
    """线程安全地将数据写入 JSONL 文件"""
    with lock:  # 只有一个线程能进入
        with open(filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")  # 确保 JSON 格式正确