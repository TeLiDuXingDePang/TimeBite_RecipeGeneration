# 调用 Coze 智能体API 的核心步骤

1. 构造 HTTP 请求
请求 URL：
基础版：https://api.coze.cn/open_api/v2/chat
专业版：https://api.coze.cn/v3/chat（支持流式响应）。

请求头：
```json
{
  "Authorization": "Bearer {{Personal_Access_Token}}",
  "Content-Type": "application/json"
}
```

请求体示例：
```json
{
  "bot_id": "7487100580821893160",  // 机器人ID，用于区分不同的聊天机器人
  "user": "unique_user_identifier",  // 用户唯一标识符
  "query": "你好，今天天气如何？",  // 用户查询内容
  "stream": false  // 是否启用流式响应，基础版不支持流式响应
}
```

2. 处理响应
普通响应：返回 JSON 格式的完整回复，包含messages数组和状态码。

示例代码：
```python
import requests
import json

def send_request_to_coze(query, token):
    url = "https://api.coze.cn/open_api/v2/chat"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "bot_id": "7487100580821893160",  # 替换为您的机器人ID
        "user": "user_123456",  # 用户标识符
        "query": query,  # 用户查询内容
        "stream": False  # 基础版不支持流式响应
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # 检查请求是否成功
        
        response_data = response.json()
        
        # 从响应中提取消息
        messages = response_data.get('messages', [])
        
        # 获取助手的回复
        for message in messages:
            if message.get('role') == 'assistant':
                return message.get('content', '')
        
        return "未找到助手回复"
        
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return f"API请求失败: {str(e)}"
    except Exception as e:
        print(f"处理响应时出错: {e}")
        return f"处理响应时出错: {str(e)}"

# 示例使用
token = "your_personal_access_token"
query = "请提供红烧肉的菜谱"
response = send_request_to_coze(query, token)
print(response)
```

对于专业版的流式响应处理示例：
```python
import requests
import json

def stream_response_from_coze(query, token):
    url = "https://api.coze.cn/v3/chat"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "bot_id": "your_bot_id",
        "user": "user_123456",
        "query": query,
        "stream": True  # 启用流式响应
    }

    response = requests.post(url, headers=headers, json=payload, stream=True)
    
    full_content = ""
    for chunk in response.iter_lines(chunk_size=8192):
        if chunk:
            try:
                event = json.loads(chunk)
                if event.get("event") == "message":
                    content = event.get("data", {}).get("content", "")
                    full_content += content
                    print("接收到数据片段...")
            except json.JSONDecodeError:
                print(f"无法解析JSON: {chunk}")
    
    return full_content
```

3. 使用响应内容
响应中的content字段可能包含结构化数据(JSON格式)，您可以解析它并按需使用，例如菜谱信息：

```json
{
    "name": "红烧肉",
    "cook_time": "60",
    "calories": "约500千卡/100克",
    "image": "https://s.coze.cn/t/r0lJIxATG-I/",
    "description": "红烧肉色泽红亮，肥而不腻，入口即化，是一道经典的传统名菜。",
    "steps": [
        {
            "step": 1,
            "content": "将五花肉切成大小均匀的方块，冷水下锅，加入姜片、料酒，大火煮开后撇去浮沫，捞出用清水冲洗干净。"
        },
        {
            "step": 2,
            "content": "锅中倒少许油，放入冰糖，小火慢慢翻炒，待冰糖融化变成焦糖色时，迅速将焯好水的五花肉块放入锅中，翻炒均匀，让每块肉都裹上糖色。"
        },
        {
            "step": 3,
            "content": "加入葱段、姜片、八角、桂皮、香叶、干辣椒，继续翻炒出香味。"
        },
        {
            "step": 4,
            "content": "倒入适量生抽、老抽，翻炒均匀，使肉块充分上色。"
        },
        {
            "step": 5,
            "content": "加入没过肉块的热水，大火煮开后转小火，盖上锅盖，炖煮40 - 50分钟，直到肉质软烂。"
        },
        {
            "step": 6,
            "content": "打开锅盖，转大火收汁，期间不断翻炒，让汤汁变得浓稠，包裹在每块肉上即可出锅装盘。"
        }
    ],
    "difficulty": "中等"
}
```

示例：解析并使用菜谱数据
```python
try:
    # 假设response是从API获取的菜谱JSON字符串
    recipe_data = json.loads(response)
    
    print(f"菜谱名称: {recipe_data.get('name')}")
    print(f"烹饪时间: {recipe_data.get('cook_time')} 分钟")
    print(f"热量: {recipe_data.get('calories')}")
    
    print("\n烹饪步骤:")
    for step in recipe_data.get('steps', []):
        print(f"步骤 {step.get('step')}: {step.get('content')}")
except json.JSONDecodeError:
    print("响应不是有效的JSON格式")
```

4. 注意事项
- 确保正确设置Authorization头部，使用Bearer前缀和您的个人访问令牌
- 使用正确的bot_id，这是您在Coze平台上创建的机器人ID
- 对于基础版API，stream参数应设置为false
- 请求中的user字段用于标识用户，可以使用任意唯一标识符
- 使用query字段直接传递用户的问题或指令，而不是使用messages数组