import requests
import json
import re

# 正则表达式
def extract_python_code(text):
    pattern = r'```python\s*(.*?)\n```'
    code_blocks = re.findall(pattern, text, re.DOTALL)
    if code_blocks:
        return code_blocks[0]
    else:
        pass

# 模式选择，debug模式和普通模式

# mode = "debug"
mode = "default"

# post请求头，用于用户认证
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 114514"
}

# post请求体数据，包括对话信息
data = {
    "messages": "",
    "model": "rwkv",
    "stream": False,
    "max_tokens": 1000,
    "temperature": 1
}

def ai(messages):
    url = "http://127.0.0.1:8000/chat/completions"  # 设置LCChat的api地址
    data["messages"] = messages
    # 发送post请求
    response = requests.post(url, headers=headers, data=json.dumps(data))  # 发送 POST 请求并获取响应对象

    r = json.loads(response.text)
    if mode == "default":
        return r["choices"][0]["message"]
    else:
        return r

# 初始化messages
messages = [{"role": "system", "content": "你是一个智能助手，名为云言轻语，神通广大！"}]

# 无限循环对话
while True:
    # 获取用户输入
    user_input = input("> ")
    user_message = {"role": "user", "content": user_input}
    # 将用户输入添加到messages中
    messages.append(user_message)

    # If it's the first interaction, send the initial message
    if len(messages) == 2:
        initial_message = {"role": "assistant", "content": "请使用python解决以下问题，请使用markdown格式回复"}
        messages.append(initial_message)

    # 发送API请求
    response = ai(messages)
    # 输出API返回内容
    if mode == "default":
        print("LCChat:", response["content"])
        if extract_python_code(response["content"]):
            print("\n\n运行结果\n\n")
            exec(extract_python_code(response["content"]))
        else:
            pass

    else:
        print("调试数据：\n")
        print("获得的json:", response)

    # 将API接口返回的内容添加至messages，以用作多轮对话
    if mode == "default":
        messages.append(response)
    else:
        data["messages"] = messages
        print("发送给服务器的对话记录：", data)
        messages.append(response["choices"][0]["message"])

        print("\n\n正常对话：\n")
        print("User:", user_input)
        print("LCChat:", response["choices"][0]["message"]["content"])
    # 如果API返回的内容包含"goodbye"，则结束对话循环
    if "goodbye" in user_input:
        print("Goodbye!")
        break