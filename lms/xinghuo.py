from api import SparkApi
from lib import extractCodeFromResponse as exe
import config as conf
#以下密钥信息从控制台获取
appid = conf.api["xinghuo"]["appid"]     #填写控制台中获取的 APPID 信息
api_secret = conf.api["xinghuo"]["api_secret"]   #填写控制台中获取的 APISecret 信息
api_key = conf.api["xinghuo"]["api_key"]    #填写控制台中获取的 APIKey 信息

#用于配置大模型版本，默认“general/generalv2”
domain = conf.api["xinghuo"]["domain"]   # v1.5版本
# domain = "generalv2"    # v2.0版本
#云端环境的服务地址
Spark_url = conf.api["xinghuo"]["Spark_url"]  # v1.5环境的地址
# Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址

text =[]

# length = 0

def getText(role,content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text
    
def clear():
    global text
    text = []

def main(prompt):
    question = checklen(prompt)
    SparkApi.answer =""
    print("星火:",end = "")
    SparkApi.main(appid,api_key,api_secret,Spark_url,domain,question)
    response = getText("assistant",SparkApi.answer)
    r = 0
    if exe.extract_python_code(SparkApi.answer):  
        r = exe.extract_python_code(SparkApi.answer)
        print(r)
    else:
        pass
    
    if r:
        return {
            "response": response,
            "result": r
        }
    else:
        return{
            "response": response,
            "result": "print(\"无需执行\")"
        }
    
