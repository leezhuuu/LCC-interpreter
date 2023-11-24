from lms import config as conf
import os

print(conf.config)

# 选择ai模型
api = "xinghuo"
# api = "ChatGPT"
# api = "rwkv"


if __name__ == '__main__':
    # 根据选择启动对应模型
    if api == "xinghuo":
        # os.system("streamlit run front.py && start http://localhost:8501/?model=xinghuo")
        # os.system("python ./lms/xinghuo_console.py")
        os.system("python ./lms/xinghuo_http.py")
    elif api == "ChatGPT":
        os.system("streamlit run front.py && start http://localhost:8501/?model=ChatGPT")
    elif api == "rwkv":
        os.system("streamlit run front.py && start http://localhost:8501/?model=rwkv")
