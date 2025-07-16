from flask import Flask, request, jsonify, render_template
from garden_interpreter import parse_program, execute

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

@app.route('/interpreter')
def interpreter():
    return render_template('interpreter.html')

@app.route('/run', methods=['POST'])
def run_code():
    source = request.json['code']
    try:
        program, functions, function_labels = parse_program(source)
        result = execute(program, functions, function_labels)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'harvest': '',
            'error': f'Parsing error: {str(e)}'
        })

if __name__ == '__main__':
    app.run(debug=True)