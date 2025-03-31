import requests
import json

def get_recipe(recipe_name, token):
    """
    调用智能体API获取菜谱信息
    
    参数:
        recipe_name: 要查询的菜谱名称
        token: 个人访问令牌
    
    返回:
        解析后的菜谱信息
    """
    # API请求URL
    url = "https://api.coze.cn/open_api/v2/chat"
    
    # 设置请求头
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 根据示例代码构造请求体
    payload = {
        "bot_id": "7487100580821893160",
        "user": f"user_{abs(hash(recipe_name)) % 10000000}",  # 用户标识
        "query": f"{recipe_name}",
        "stream": False
    }
    
    print(f"发送请求到: {url}")
    print(f"请求头: {headers}")
    print(f"请求体: {json.dumps(payload, ensure_ascii=False, indent=2)}")
    
    try:
        # 发送请求
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # 检查请求是否成功
        
        print(f"响应状态码: {response.status_code}")
        
        # 解析响应数据
        response_data = response.json()
        print(f"完整响应数据: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
        
        # 从响应中提取消息
        messages = response_data.get('messages', [])
        
        # 查找assistant角色且type为answer的消息内容
        for message in messages:
            if message.get('role') == 'assistant' and message.get('type') == 'answer':
                message_content = message.get('content', '')
                print(f"提取的answer内容: {message_content}")
                
                # 尝试解析JSON内容
                try:
                    recipe_data = json.loads(message_content)
                    return recipe_data
                except json.JSONDecodeError:
                    # 如果不是JSON格式，直接返回文本内容
                    return message_content
        
        return "未找到answer类型的助手回复"
        
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return f"API请求失败: {str(e)}"
    except Exception as e:
        print(f"处理响应时出错: {e}")
        return f"处理响应时出错: {str(e)}"

def print_recipe(recipe_data):
    """
    格式化打印菜谱信息
    
    参数:
        recipe_data: 菜谱数据字典
    """
    if isinstance(recipe_data, str):
        print("获取到的原始响应:")
        print(recipe_data)
        return
    
    print("\n" + "="*50)
    print(f"【菜谱名称】: {recipe_data.get('name', '未知')}")
    print(f"【烹饪时间】: {recipe_data.get('cook_time', '未知')} 分钟")
    print(f"【热量】: {recipe_data.get('calories', '未知')}")
    print(f"【难度】: {recipe_data.get('difficulty', '未知')}")
    print(f"【图片链接】: {recipe_data.get('image', '无')}")
    print("\n【菜品描述】")
    print(recipe_data.get('description', '无描述'))
    
    print("\n【烹饪步骤】")
    steps = recipe_data.get('steps', [])
    for step in steps:
        print(f"步骤 {step.get('step', '?')}: {step.get('content', '')}")
    
    print("="*50 + "\n")

if __name__ == "__main__":
    # 使用提供的令牌
    token = "pat_YTZ66uuJRvL42sxcb8HEfTRMSuSIkjuHcjCX3jDOwnyYroO49dlKRhQDPnUiRJ17"
    
    # 获取用户输入菜谱名称
    recipe_name = input("请输入要查询的菜谱名称: ")
    
    # 调用API获取菜谱
    recipe_data = get_recipe(recipe_name, token)
    
    # 打印菜谱信息
    print_recipe(recipe_data) 