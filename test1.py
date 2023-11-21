import requests
import json
import subprocess

api_key = "fk-mcwP2-UJJxzzr60_pE1jRJXErwy_YSFsWHYw51Efgb4"
api_endpoint = "https://ai.fakeopen.com/v1/chat/completions"
# 设置请求头
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# 设置请求体
def get_user_input():
    # user_input = input("请输入一个问题或指令: ")
    user_input = input()
    return user_input

def get_ai_response(user_input):
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "你是由chatgpt驱动的codeinterpreter，当前系统为macos,每次收到用户的信息时，请判断你的工作模式，再进行相应的任务。你有两个模式，模式一：用户向你发出可执行指令，则使用python程序（优先）或者bash命令完成相应任务，请只回答代码，不要回复其他内容；模式二：用户想和你进行对话，请正常对话，不要输出任何形式的代码，自然地、严谨的语气与用户进行对话。每次收到用户的信息时，请判断你的工作模式，再进行相应的任务。"},
            # {"role": "system", "content": "你是由chatgpt驱动的codeinterpreter"},
            {"role": "user", "content": user_input}
        ]
    }

    # 发送POST请求
    response = requests.post(api_endpoint, headers=headers, data=json.dumps(data))

    # 解析响应
    result = response.json()
    ai_response = result["choices"][0]["message"]["content"]

    return ai_response

def execute_code(code):
    if code.startswith('```python') and code.endswith('```'):
        python_code = code[10:-3]  # 剥离Python代码块的标记
        try:
            exec(python_code)
        except Exception as e:
            print(f"执行Python代码时发生错误: {e}")
    elif code.startswith('```bash') and code.endswith('```'):
        shell_command = code[8:-3]  # 剥离Shell命令的标记
        try:
            # 使用Colab的内置功能执行Shell命令
            output = subprocess.getoutput(shell_command)
            print(output)
        except Exception as e:
            print(f"执行Shell命令时发生错误: {e}")
    else:
        print("未知类型的代码")

def main():
    while True:
        user_input = get_user_input()
        if user_input.lower() == 'exit':
            print("程序结束。")
            break

        ai_response = get_ai_response(user_input)
        # print("AI生成的代码:")
        print(ai_response)

        execute_code(ai_response)

if __name__ == "__main__":
    main()