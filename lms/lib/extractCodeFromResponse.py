import re

def extract_python_code(text):
    pattern = r'```python\s*(.*?)\n```'
    code_blocks = re.findall(pattern, text, re.DOTALL)
    if code_blocks:
        return code_blocks[0]

def extract_bash_code(text):
    pattern = r'```bash\s*(.*?)\n```'
    code_blocks = re.findall(pattern, text, re.DOTALL)
    if code_blocks:
        return code_blocks[0]
    
def extract_c_code(text):
    pattern = r'```c\s*(.*?)\n```'
    code_blocks = re.findall(pattern, text, re.DOTALL)
    if code_blocks:
        return code_blocks[0]