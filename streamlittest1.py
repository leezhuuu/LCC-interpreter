import streamlit as st
import subprocess
import os
import requests
import json

# 设置Python脚本的路径
script_path = "/Users/happy/Documents/项目/正在测试的项目/leezhuuu_lcinterpreter/v4/test_v1.py"

api_key = "fk-mcwP2-UJJxzzr60_pE1jRJXErwy_YSFsWHYw51Efgb4"
api_endpoint = "https://ai.fakeopen.com/v1/chat/completions"
# 设置请求头
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

def get_ai_response(user_input):
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "你是由chatgpt驱动的codeinterpreter，当前系统为macos。你有两个模式，模式一：用户向你发出可执行指令，则使用python程序（优先）或者bash命令完成相应任务，请只回答代码，不要回复其他内容；模式二：用户想和你进行对话，请正常对话，不要输出任何形式的代码，自然地、严谨的语气与用户进行对话。每次收到用户的信息时，请判断你的工作模式，再进行相应的任务。在模式一中，你需要理解用户的请求，完善、丰富用户的命令，然后执行。执行完后，将你发给自己的命令、你的输出以及执行结果拼接起来，发送给第二个代码的AI进行整理。"},
            {"role": "user", "content": user_input}
        ]
    }

    # 发送POST请求
    response = requests.post(api_endpoint, headers=headers, data=json.dumps(data))

    # 解析响应
    result = response.json()
    ai_response = result["choices"][0]["message"]["content"]

    return ai_response

def run_script(input):
    # 使用subprocess运行脚本并获取输出
    process = subprocess.Popen(['python3', script_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = process.communicate(input.encode('utf-8'))
    return out.decode('utf-8')

st.title('Python脚本交互')

# 创建一个输入框
user_input = st.text_input("请输入您的文本：")

if st.button('提交'):
    # 当用户点击提交按钮时，运行脚本并显示输出
    ai_command = get_ai_response(user_input)
    output = run_script(ai_command)
    st.code(ai_command)  # 使用st.code显示输入
    st.write(output)  # 使用st.write显示输出