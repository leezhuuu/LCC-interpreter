import streamlit as st
import sys
sys.path.append('./lms')
sys.path.append('./')
from lms import xinghuo

st.title("💬 LCC Chatbot")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")
conf = st.experimental_get_query_params()
print(conf)
print(st.session_state)
xinghuo.clear()

def responseFromApi(apiName, prompt):
    if apiName == "xinghuo":        
        return xinghuo.main(prompt)
    pass


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    msg = responseFromApi(conf["model"][0], st.session_state["messages"])
    st.session_state.messages.append({"role": "assistant", "content": msg["response"][-1]["content"]})
    st.chat_message("assistant").write(msg["response"][-1]["content"])
    try:  
        if "result" in msg:  
            # print("yes")  
            # 获取用户输入的代码  
            code = msg["result"]
            exec(code)
            # 在聊天窗口中输出执行结果  
            # st.chat_message("assistant").write(f"输出结果：\n{result}")

        else:  
            print("no result")  
    except Exception as e:  
        print("An error occurred: ", e)
