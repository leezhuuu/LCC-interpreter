import streamlit as st
import requests
import json
import subprocess

# 在这里设置是否显示代码片段
show_code = False

# 在这里设置是否显示聊天记录
show_chat_history = False

api_key = xxxxxxxx
api_endpoint = xxxxxxxx

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# 检查是否已经有一个名为'chat_history'的session_state
if 'chat_history' not in st.session_state:
    # 如果没有，就创建一个
    st.session_state['chat_history'] = []

def get_user_input():
    user_input = st.text_input("请输入一个问题或指令: ")
    return user_input

def get_ai_response(user_input):
    # 每次对话开始时，先添加系统提示
    st.session_state['chat_history'].append({"role": "system", "content": "你是由chatgpt驱动的codeinterpreter，当前系统为linux,环境为python3，执行相应任务时，请使用streamlit库实现信息的输出,只用输出python代码，不要回复、输出其他任何形式的文本内容.当user没有向你做出任何指令时，只回复：“很高兴为您服务！”"})
    
    # 将用户的输入添加到聊天记录中
    st.session_state['chat_history'].append({"role": "user", "content": user_input})

    # 如果聊天记录超过2000字，只保留前2000字
    if len(''.join([message["content"] for message in st.session_state['chat_history']])) > 4000:
        while len(''.join([message["content"] for message in st.session_state['chat_history']])) > 4000:
            st.session_state['chat_history'].pop(0)

    data = {
        "model": "gpt-3.5-turbo",
        "messages": st.session_state['chat_history']
    }

    response = requests.post(api_endpoint, headers=headers, data=json.dumps(data))
    result = response.json()
    ai_response = result["choices"][0]["message"]["content"]

    # 将AI的回应添加到聊天记录中
    st.session_state['chat_history'].append({"role": "assistant", "content": ai_response})

    # 打印聊天记录
    if show_chat_history:
        st.write("聊天记录:")
        for message in st.session_state['chat_history']:
            st.write(f"{message['role']}: {message['content']}")

    return ai_response

def execute_code(code):
    if code.startswith('```python') and code.endswith('```'):
        python_code = code[10:-3]
        try:
            exec(python_code)
        except Exception as e:
            st.error(f"执行Python代码时发生错误: {e}")
    elif code.startswith('```bash') and code.endswith('```'):
        shell_command = code[8:-3]
        try:
            output = subprocess.getoutput(shell_command)
            st.write(output)
        except Exception as e:
            st.error(f"执行Shell命令时发生错误: {e}")
    else:
        st.warning("未执行任何操作。")

def main():
    st.title("Code Interpreter")
    st.write("你好，我是Leezhu制作的code-interpreter，拥有代码生成、数学计算等功能。是下一代贾维斯的基座引擎。请问有什么我可以帮您的吗？")
    user_input = get_user_input()
    if user_input.lower() == 'exit':
        st.stop()
    else:
        ai_response = get_ai_response(user_input)
        if show_code:  # 根据show_code变量的值决定是否显示代码片段
            st.code(ai_response)
        execute_code(ai_response)

if __name__ == "__main__":
    main()
