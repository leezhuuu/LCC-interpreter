import uuid

def save_code_to_file(text):
    file_name = str(uuid.uuid4())
    with open(file_name, 'w') as f:
        f.write(text)
    return file_name

# 示例
# text = "这是一个示例文本。"
# file_name = save_code_to_file(text)
# print(f"文本已保存到文件：{file_name}")
