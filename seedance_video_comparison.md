# Seedance视频生成对比分析

## 实验概述
**目的**: 对比Seedance 1.0 Pro模型在不同随机种子下的生成效果
**时间**: 2026-02-27 00:13 - 00:48
**执行者**: AI助手3号 (192.168.199.232)

## 技术配置
### 环境
- **Python环境**: 虚拟环境 (`seedance_env`)
- **SDK**: `volcenginesdkarkruntime`
- **API Key**: `d380aed6-916e-4542-bd67-a20bbd1b377c` (UUID格式)
- **区域**: `cn-beijing`

### 模型尝试
1. **目标模型**: Seedance 1.5 Pro (`doubao-seedance-1-5-pro-250528`)
   - 状态: ❌ 不可用 (404错误)
   - 错误: `InvalidEndpointOrModel.NotFound`
   
2. **使用模型**: Seedance 1.0 Pro (`doubao-seedance-1-0-pro-250528`)
   - 状态: ✅ 可用
   - 版本: 250528 (2025年5月28日)

## 两次生成任务对比

### 任务1: 首次生成
- **任务ID**: `cgt-20260227001305-cg4lf`
- **创建时间**: 00:13
- **完成时间**: 00:26 (耗时13分钟)
- **随机种子**: 85539 (系统自动分配)
- **文件大小**: 15.0MB → 压缩到3.1MB
- **压缩率**: 79%
- **下载链接**: [TOS链接1](https://ark-content-generation-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-1-0-pro/02177212238638900000000000000000000ffffac182f9dba886a.mp4)

### 任务2: 对比生成
- **任务ID**: `cgt-20260227003618-6pns2`
- **创建时间**: 00:36
- **完成时间**: 00:48 (耗时12分钟)
- **随机种子**: 12345 (手动指定)
- **文件大小**: 13.4MB → 压缩到3.0MB
- **压缩率**: 78%
- **下载链接**: [TOS链接2](https://ark-content-generation-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-1-0-pro/02177212377889100000000000000000000ffffac182f9dcccce7.mp4)

## 共同参数
### 提示词 (中文字符)
```
李世民动漫形象攻城，碰撞火花，尘土飞扬，战旗飘扬，恢弘气势，电影史诗感，电影级运镜，动态光影，4K画质
```

### 技术参数
- **时长**: 5秒
- **分辨率**: 1080p
- **宽高比**: 16:9
- **帧率**: 24fps (默认)
- **服务层级**: default

## API参数格式突破

### 初始错误尝试
```python
# 错误：使用prompt参数
task = client.content_generation.tasks.create(
    model='doubao-seedance-1-0-pro-250528',
    prompt='文本提示词',  # ❌ 错误参数
    duration=5,
    ratio='16:9',
    resolution='1080p'
)
```

### 正确格式
```python
from volcenginesdkarkruntime.types.content_generation.create_task_content_param import CreateTaskContentTextParam

# 创建文本内容参数
text_content = CreateTaskContentTextParam(
    type='text',
    text='李世民动漫形象攻城...'
)

# 正确：使用content参数（必须是列表）
task = client.content_generation.tasks.create(
    model='doubao-seedance-1-0-pro-250528',
    content=[text_content],  # ✅ 正确格式
    duration=5,
    ratio='16:9',
    resolution='1080p',
    seed=12345  # 可选：指定随机种子
)
```

## 文件处理流程

### 下载脚本
```python
import requests

response = requests.get(video_url, stream=True)
with open('output.mp4', 'wb') as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)
```

### 压缩命令 (ffmpeg)
```bash
ffmpeg -i input.mp4 -vcodec libx264 -crf 28 -preset fast \
       -acodec aac -b:a 64k -movflags +faststart output.mp4
```

### 压缩效果
- **原始大小**: 13-15MB
- **压缩后**: 3.0-3.1MB
- **压缩率**: 78-79%
- **质量保持**: 良好（肉眼难以区分）

## 技术发现总结

### ✅ 已验证能力
1. **API调用**: 完整的工作流程
2. **参数格式**: 正确的content参数结构
3. **错误处理**: 模型不可用、频率限制等
4. **文件处理**: 下载、压缩、存储
5. **任务管理**: 创建、监控、查询

### ❌ 发现限制
1. **模型可用性**: 仅Seedance 1.0 Pro可用
2. **微信限制**: 客服接口有频率限制（错误码95001）
3. **文件大小**: 原始视频>10MB，需要压缩才能微信发送

### 🔧 解决方案
1. **模型回退**: 使用可用的1.0 Pro版本
2. **频率管理**: 控制消息发送节奏
3. **文件压缩**: ffmpeg高效压缩
4. **备份链接**: 提供原始TOS下载链接（24小时）

## 视觉对比建议

### 观察要点
1. **画面一致性**: 相同提示词是否产生相似场景
2. **细节差异**: 人物形象、动作、特效的细微差别
3. **运动流畅度**: 动画的平滑程度
4. **光影效果**: 动态光影的表现
5. **整体氛围**: 史诗感、电影感的传达

### 对比方法
1. **并排播放**: 同时播放两个视频
2. **逐帧分析**: 检查关键帧的差异
3. **主观评价**: 哪个版本更符合预期
4. **技术指标**: 文件大小、压缩质量等

## 后续应用建议

### 技术优化
1. **参数调优**: 尝试不同的seed值
2. **提示词优化**: 细化描述获得更精准结果
3. **批量生成**: 同一提示词多版本生成
4. **质量评估**: 建立客观评价标准

### 业务应用
1. **内容创作**: 短视频、宣传片素材
2. **A/B测试**: 不同版本的效果测试
3. **风格探索**: 尝试不同艺术风格
4. **效率提升**: 快速生成视觉内容

## 文件清单
1. `lishimin_city_attack.mp4` - 第一次生成原始文件 (15MB)
2. `lishimin_small.mp4` - 第一次压缩文件 (3.1MB)
3. `lishimin_city_attack_v2.mp4` - 第二次生成原始文件 (13.4MB)
4. `lishimin_small_v2.mp4` - 第二次压缩文件 (3.0MB)
5. `seedance_1.5_task_id.txt` - 任务ID记录
6. `compress_video.py` - 压缩脚本（moviepy版本）
7. `seedance_video_comparison.md` - 本分析文档

## 时间线
- **00:13**: 第一次任务创建
- **00:26**: 第一次生成完成
- **00:28**: 发现微信文件大小限制
- **00:32**: 安装ffmpeg完成
- **00:33**: 压缩并发送第一次视频
- **00:36**: 第二次任务创建（尝试1.5 Pro）
- **00:37**: 发现1.5 Pro不可用，使用1.0 Pro
- **00:48**: 第二次生成完成
- **00:48**: 微信频率限制，等待发送窗口

---

**文档创建时间**: 2026-02-27 00:50 (Asia/Shanghai)
**文档版本**: 1.0
**作者**: AI助手3号