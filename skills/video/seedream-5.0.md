# Seedream 5.0 lite 图像生成模型

**发布时间**: 2026-02-25
**厂商**: 字节跳动/火山引擎
**状态**: ✅ 正式对外发布

---

## 🎯 核心能力

### 1. 实时检索能力 (重磅新功能!)
- **首次搭载联网检索功能**
- 配置 `tools: [{type: "web_search"}]`
- 模型根据提示词自主判断是否搜索
- **应用场景**: 生成当下热点、最新产品、实时事件相关图像

### 2. 生成模式

| 模式 | 说明 | 配置 |
|------|------|------|
| **文生图** | 纯文本提示词生成单图 | `sequential_image_generation: disabled` |
| **单图生图** | 1张参考图+文本 → 单图 | `image: "url"` + disabled |
| **多图生图** | 2-14张参考图+文本 → 单图 | `image: ["url1","url2"]` + disabled |
| **文生组图** | 文本 → 一组关联图(最多15张) | `sequential_image_generation: auto` |
| **单图生组图** | 1张参考图 → 一组关联图(最多14张) | `image: "url"` + auto |
| **多图生组图** | 多张参考图 → 一组关联图 | 输入+输出总数≤15 |

### 3. 一致性增强
- 跨图像保持角色特征
- 风格与细节高度统一
- 组图功能天然保持一致性

---

## 🔧 API调用

### 请求地址
```
POST https://ark.cn-beijing.volces.com/api/v3/images/generations
```

### 鉴权
- 仅支持 API Key 鉴权
- 获取地址: https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey

### 模型ID
| 模型 | Model ID | 特点 |
|------|----------|------|
| **Seedream 5.0 lite** | `doubao-seedream-5.0-lite` | 联网检索、组图、流式输出 |
| Seedream 4.5 | `doubao-seedream-4.5` | 组图、4K输出 |
| Seedream 4.0 | `doubao-seedream-4.0` | 组图、1K-4K输出 |
| Seedream 3.0 t2i | `doubao-seedream-3.0-t2i` | 文生图 |
| Seededit 3.0 i2i | `doubao-seededit-3.0-i2i` | 图生图 |

---

## 📋 请求参数

### 必需参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `model` | string | 模型ID,如 `doubao-seedream-5.0-lite` |
| `prompt` | string | 提示词,支持中英文,建议≤300汉字或600英文单词 |

### 图像输入参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `image` | string/array | 参考图URL或Base64,5.0支持1-14张 |

**图片要求**:
- 格式: jpeg, png, webp, bmp, tiff, gif (5.0新增后四种)
- 宽高比: [1/16, 16]
- 宽高像素: >14px
- 大小: ≤10MB
- 总像素: ≤6000×6000=36000000px

### 尺寸参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `size` | string | 图像尺寸 |

**5.0 lite 尺寸选项**:

方式1 - 指定分辨率:
- `2K` 或 `3K`,配合prompt描述宽高比

方式2 - 指定像素值:
- 默认: `2048x2048`
- 总像素范围: [3686400, 10404496]
- 宽高比范围: [1/16, 16]

**推荐尺寸**:

| 分辨率 | 宽高比 | 像素值 |
|--------|--------|--------|
| 2K | 1:1 | 2048x2048 |
| 2K | 4:3 | 2304x1728 |
| 2K | 3:4 | 1728x2304 |
| 2K | 16:9 | 2848x1600 |
| 2K | 9:16 | 1600x2848 |
| 3K | 1:1 | 3072x3072 |
| 3K | 4:3 | 3456x2592 |
| 3K | 16:9 | 4096x2304 |
| 3K | 9:16 | 2304x4096 |

### 组图参数 (5.0独有)

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `sequential_image_generation` | string | disabled | `auto`开启组图,`disabled`单图 |
| `sequential_image_generation_options.max_images` | int | 15 | 最多生成图片数[1,15] |

### 联网搜索 (5.0独有)

| 参数 | 类型 | 说明 |
|------|------|------|
| `tools` | array | `[{type: "web_search"}]` 开启联网 |

### 其他参数

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `stream` | bool | false | 流式输出(5.0/4.5/4.0支持) |
| `output_format` | string | jpeg | 输出格式: png/jpeg (仅5.0) |
| `response_format` | string | url | 返回格式: url/b64_json |
| `watermark` | bool | true | 是否添加"AI生成"水印 |
| `optimize_prompt_options.mode` | string | standard | 提示词优化: standard/fast |

---

## 📤 响应参数

```json
{
  "model": "doubao-seedream-5.0-lite-xxxxxx",
  "created": 1740484800,
  "data": [
    {
      "url": "https://...",  // response_format=url时
      "b64_json": "...",     // response_format=b64_json时
      "size": "2048x2048"
    }
  ],
  "tools": [
    {"type": "web_search"}
  ],
  "usage": {
    "generated_images": 1,
    "output_tokens": 16384,
    "total_tokens": 16384,
    "tool_usage": {
      "web_search": 1  // 实际搜索次数
    }
  }
}
```

**注意**: URL链接24小时内有效,请及时下载!

---

## 💻 Python调用示例

```python
from volcenginesdkarkruntime import Ark

client = Ark(api_key='your-api-key')

# 基础文生图
response = client.images.generate(
    model='doubao-seedream-5.0-lite',
    prompt='一只可爱的橘猫在阳光下打盹,摄影风格,4K高清',
    size='2048x2048',
    response_format='url'
)

print(response.data[0].url)

# 联网搜索生图
response = client.images.generate(
    model='doubao-seedream-5.0-lite',
    prompt='2026年最新款iPhone手机,产品摄影,白色背景',
    size='2K',
    tools=[{'type': 'web_search'}],
    response_format='url'
)

# 组图生成
response = client.images.generate(
    model='doubao-seedream-5.0-lite',
    prompt='一个红衣女孩在巴黎旅行的一天,从早到晚的不同场景',
    size='2K',
    sequential_image_generation='auto',
    sequential_image_generation_options={'max_images': 6},
    response_format='url'
)

for i, img in enumerate(response.data):
    print(f"图{i+1}: {img.url}")

# 多图融合生图
response = client.images.generate(
    model='doubao-seedream-5.0-lite',
    prompt='将这些元素融合成一张创意海报',
    image=[
        'https://example.com/image1.jpg',
        'https://example.com/image2.jpg'
    ],
    size='2048x2048',
    response_format='url'
)
```

---

## 🔄 与Seedance视频工作流整合

```
┌─────────────────────────────────────────┐
│ 1. Seedream 5.0 生成参考图/首帧          │
│    - 联网搜索获取最新素材                 │
│    - 组图功能生成分镜参考                 │
│                ↓                        │
│ 2. 选择最佳图片作为Seedance输入          │
│                ↓                        │
│ 3. Seedance 2.0 生成视频                │
│    - @Image1 作为首帧                   │
│    - 保持角色一致性                      │
└─────────────────────────────────────────┘
```

**组图→分镜**:
```python
# 用Seedream生成分镜参考图
response = client.images.generate(
    model='doubao-seedream-5.0-lite',
    prompt='一个穿越唐朝的现代女孩的故事,分为6个场景:1.现代办公室 2.穿越时空隧道 3.唐朝宫殿 4.集市探索 5.学习唐朝礼仪 6.返回现代',
    sequential_image_generation='auto',
    sequential_image_generation_options={'max_images': 6}
)

# 每张图作为Seedance视频的首帧
for i, img in enumerate(response.data):
    # 用这张图生成对应场景的视频
    pass
```

---

## 📚 相关链接

- API文档: https://www.volcengine.com/docs/82379/1541523
- 流式响应: https://www.volcengine.com/docs/82379/1824137
- 控制台: https://console.volcengine.com/ark/region:ark+cn-beijing/
- API Key获取: https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey

---

_技能版本: v1.0_
_创建时间: 2026-02-25 12:58 UTC_
_状态: ✅ 完整文档_
_维护者: 贾维斯_
