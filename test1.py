from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_post():
    print("Headers:")
    for key, value in request.headers:
        print(f"{key}: {value}")
    
    print("Data:")
    data = request.get_json()
    print(data)
    
    code = data.get('data', {}).get('代码', '')
    code = code.replace('```python\n', '').replace('\n```', '')  # remove markdown code block tags
    exec(code)  # execute the code
    
    return jsonify({"test": "test111"}), 200

if __name__ == "__main__":
    app.run()