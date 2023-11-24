import requests
import json
from lib import extractCodeFromResponse as exe
import config as conf
apikey = conf.api["RWKV"]["aipkey"]
model = conf.api["RWKV"]["model"]
apiurl = conf.api["RWKV"]["apiurl"]

# post请求头，用于用户认证
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + apikey 
}

# post请求体数据，包括对话信息
data = {
    "messages": "",
    "model": model,
    "stream": False,
    "max_tokens": 1000,
    "temperature": 1
}

def ai(messages):
    url = apiurl  # 设置LCChat的api地址
    data["messages"] = messages
    # 发送post请求
    response = requests.post(url, headers=headers, data=json.dumps(data))  # 发送 POST 请求并获取响应对象

    r = json.loads(response.text)
    return r["choices"][0]["message"]

# 初始化messages
messages = [{"role": "system", "content": "你是一个智能助手，名为云言轻语，神通广大！"}]

# 无限循环对话
while True:
    # 获取用户输入
    user_input = input("我：")
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
    print("AI：", response["content"])
    if exe.extract_python_code(response["content"]):
        print("\n\n运行结果\n\n")
        exec(exe.extract_python_code(response["content"]))
    else:
        pass


    # 将API接口返回的内容添加至messages，以用作多轮对话
    messages.append(response)
    
    # 如果API返回的内容包含"goodbye"，则结束对话循环
    if "goodbye" in user_input:
        print("Goodbye!")
        break