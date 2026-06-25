# Seedance API 接入教程

火山引擎 Seedance 视频生成 API 快速接入指南。

## 一、准备工作

### 1. 注册火山引擎账号
- 访问 https://console.volcengine.com
- 注册并完成实名认证

### 2. 获取 API Key
- 进入控制台 → 方舟大模型平台
- 创建 API Key 并保存

### 3. 安装 SDK
```bash
pip install volcengine-python-sdk[ark]
```

## 二、基础代码

### 最简示例（文生视频）

```python
from volcenginesdkarkruntime import Ark

# 初始化客户端
client = Ark(api_key="你的API_KEY")

# 创建视频生成任务
task = client.content_generation.tasks.create(
    model="doubao-seedance-1-0-pro-250528",  # Seedance 1.0
    content=[
        {"type": "text", "text": "一只猫在阳光下打盹，电影质感"}
    ]
)

print(f"任务ID: {task.id}")
```

### 查询任务状态

```python
# 查询任务
result = client.content_generation.tasks.retrieve(task.id)

print(f"状态: {result.status}")
# succeeded = 完成, running = 生成中, failed = 失败

# 完成后获取视频URL
if result.status == "succeeded":
    print(f"视频: {result.content.video_url}")
```

## 三、完整示例

```python
from volcenginesdkarkruntime import Ark
import time

API_KEY = "你的API_KEY"
MODEL = "doubao-seedance-1-0-pro-250528"

client = Ark(api_key=API_KEY)

def generate_video(prompt, duration=5, ratio="16:9"):
    """文生视频"""
    task = client.content_generation.tasks.create(
        model=MODEL,
        content=[{"type": "text", "text": prompt}],
        extra_body={"duration": duration, "ratio": ratio}
    )
    return task.id

def wait_result(task_id, timeout=300):
    """等待结果"""
    for _ in range(timeout // 10):
        result = client.content_generation.tasks.retrieve(task_id)
        if result.status == "succeeded":
            return result.content.video_url
        elif result.status == "failed":
            return None
        time.sleep(10)
    return None

# 使用
task_id = generate_video("日落海滩，海浪轻拍沙滩，4K电影质感")
print(f"任务ID: {task_id}")

video_url = wait_result(task_id)
if video_url:
    print(f"视频: {video_url}")
```

## 四、图生视频

```python
task = client.content_generation.tasks.create(
    model=MODEL,
    content=[
        {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}},
        {"type": "text", "text": "让画面动起来，镜头缓慢推进"}
    ],
    extra_body={"duration": 5}
)
```

## 五、参数说明

| 参数 | 说明 | 可选值 |
|------|------|--------|
| model | 模型ID | `doubao-seedance-1-0-pro-250528` |
| duration | 视频时长 | 5 或 10 秒 |
| ratio | 画面比例 | `16:9`, `9:16`, `1:1` |

## 六、模型版本

| 版本 | 模型ID | 状态 |
|------|--------|------|
| 1.0 | `doubao-seedance-1-0-pro-250528` | ✅ 可用 |
| 2.0 | 待开放 | ⏳ 等待 |

## 七、常见问题

**Q: 任务一直 running?**
A: 视频生成需要1-5分钟，耐心等待

**Q: 报错 unauthorized?**
A: 检查 API Key 是否正确，是否开通了模型权限

**Q: 如何提高画质?**
A: 提示词加上 `4K画质`, `电影质感`, `高清细节`

---

_教程版本: v1.0_
_适用: Seedance 1.0_
_更新: 2026-02-25_
