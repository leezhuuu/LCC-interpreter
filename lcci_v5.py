import requests
import json
import subprocess
import re
import uuid
import os
import datetime

api_endpoint = "http://47.99.140.210:5000/api/proxy"
headers = {"Content-Type": "application/json"}

log = True
conversations = {}
max_attempts = 5  # 设置最大尝试次数
save_conversations = True  # 设定是否保存对话记录

#执行代码模块
def execute_code(code, uuid_value):
    if code.startswith('```python') and code.endswith('```'):
        python_code = code[10:-3]  # 剥离Python代码块的标记
        try:
            exec(python_code)
            print("代码执行成功", flush=True)
            return True
        except Exception as e:
            print(f"执行Python代码时发生错误: {e}", flush=True)
            debug_code(uuid_value, f"执行Python代码时发生错误: {e}")
            return False
    elif code.startswith('```bash') and code.endswith('```'):
        shell_command = code[8:-3]  # 剥离Shell命令的标记
        try:
            output = subprocess.getoutput(shell_command)
            print("代码执行成功，输出结果为：", flush=True)
            print(output, flush=True)
            conversations[uuid_value].append({
                "role": "execute_coder_bash",
                "datatime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "object": "Code_execution",
                "function_name": "execute_code",
                "content": output
            })  # 保存执行结果
            return True
        except Exception as e:
            print(f"执行Shell命令时发生错误: {e}", flush=True)
            debug_code(uuid_value, f"执行Shell命令时发生错误: {e}")
            return False
    else:
        print("未知类型的代码", flush=True)
        return False

#处理用户的命令为更加丰富准确的命令
def adapt_command(user_command, uuid_value):
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "当前系统为macos,语言为简体中文，环境为python3。请利用以下prompt，在prompt中加入系统、语言、环境等信息，然后对这个prompt进行丰富完善一下细节，将用户的命令优化为一个内容更加丰富、细节更加准确的命令，输出一个新的prompt（请只输出prompt，不要输出任何无关内容）:"},
            {"role": "user", "content": user_command}
        ]
    }

    response1 = requests.post(api_endpoint, headers=headers, data=json.dumps(data))

    result1 = response1.json()
    adapted_command1 = result1["choices"][0]["message"]["content"]

    if log:
        print("对话层一的输出:", flush=True)
        print(adapted_command1, flush=True)

    conversations[uuid_value].append({
        "role": "assistant",
        "datatime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "object": f"AI_Dialogue_{len([msg for msg in conversations[uuid_value] if msg['role'] == 'assistant'])+1}",
        "function_name": "adapt_command",
        "content": adapted_command1
    })  # 保存AI对话记录

    return adapted_command1

#将优化后的命令转化为对应的可以执行的代码
def generate_code(adapted_command, uuid_value):
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "请根据以下命令生成相应的代码，以相应代码的markdown格式输出，请只输出代码内容，不要输出其他任何信息："},
            {"role": "user", "content": adapted_command}
        ]
    }

    response2 = requests.post(api_endpoint, headers=headers, data=json.dumps(data))

    result2 = response2.json()
    code = result2["choices"][0]["message"]["content"]

    if log:
        print("对话层二的输出:", flush=True)
        print(code, flush=True)

    conversations[uuid_value].append({
        "role": "assistant",
        "datatime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "object": f"AI_Dialogue_{len([msg for msg in conversations[uuid_value] if msg['role'] == 'assistant'])+1}",
        "function_name": "generate_code",
        "content": code
    })  # 保存AI对话记录

    return code

def check_and_execute_code(code, uuid_value):
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "当你不管接收任何信息，从信息中只提取代码部分，然后将代码原封不动地输出、不要输出其它任何无关信息 "},
            {"role": "user", "content": code}
        ]
    }

    response3 = requests.post(api_endpoint, headers=headers, data=json.dumps(data))

    result = response3.json()
    safecode = result["choices"][0]["message"]["content"]

    print("对话层三的输出:", flush=True)
    print(safecode, flush=True)

    conversations[uuid_value].append({
        "role": "assistant",
        "datatime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "object": f"AI_Dialogue_{len([msg for msg in conversations[uuid_value] if msg['role'] == 'assistant'])+1}",
        "function_name": "check_and_execute_code",
        "content": safecode
    })  # 保存AI对话记录

    return execute_code(safecode, uuid_value)

def save_conversations_to_json(uuid_value):
    if save_conversations:
        if not os.path.exists('aiconversation'):
            os.makedirs('aiconversation')
        with open(f'aiconversation/{uuid_value}.json', 'w', encoding='utf-8') as f:
            # 获取用户的输入内容
            abstract = next((message["content"] for message in conversations[uuid_value] if message["role"] == "user"), None)
            # 构造新的JSON格式
            new_format = {
                "uuid": uuid_value,
                "datatime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "abstract": abstract,
                "messages": conversations[uuid_value]
            }
            json.dump(new_format, f, ensure_ascii=False, indent=4)

def main():
    user_command = input("请输入一个问题或指令: ")
    if user_command.lower() == "exit program":
        print("程序结束。")
        return
    uuid_value = str(uuid.uuid4())  # 更改变量名
    conversations[uuid_value] = [{
        "role": "user",
        "datatime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "content": user_command
    }]  # 使用新的变量名
    save_conversations_to_json(uuid_value)  # 立即保存对话记录
    adapted_command = adapt_command(user_command, uuid_value)
    save_conversations_to_json(uuid_value)  # 立即保存对话记录
    code = generate_code(adapted_command, uuid_value)
    save_conversations_to_json(uuid_value)  # 立即保存对话记录
    if not check_and_execute_code(code, uuid_value):  # 使用新的变量名
        error_message = f"执行Python代码时发生错误: {e}"
        conversations[uuid_value].append({
            "role": "assistant",
            "datatime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "object": "Error_message",
            "function_name": "check_and_execute_code",
            "content": error_message
        })
    save_conversations_to_json(uuid_value)  # 立即保存对话记录

if __name__ == "__main__":
    main()






#不是的，不能单纯这样修改，你需要仔细查看原来每个函数的json是以怎样的格式保存的，注意

# 应该先出现user，然后再出现AI_Dialogue_1，然后是AI_Dialogue_2，再然后是AI_Dialogue_3，其他重复的应该去掉，以下是完整的格式
# 当是用户时，格式为"role": "user","content": ...，
# 当为ai时，格式应为"role": "assistant","content":... ,"object": "...","function_name":...
# 当为python或者bash时，则为:''execute_coder_python''或者''execute_coder_bash‘':...
# 其中，用户只出现一次