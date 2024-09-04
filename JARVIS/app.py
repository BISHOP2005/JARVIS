from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

output_data = []

@app.route('/')
def index():
    return render_template('index.html', output_data=output_data)

@app.route('/update', methods=['POST'])
def update():
    global output_data
    new_output = request.form['new_output']
    output_data.append(new_output)
    return jsonify(status="success")

@app.route('/update_output', methods=['GET'])
def update_output():
    global output_data
    return jsonify(output_data=output_data)

if __name__ == '__main__':
    app.run(debug=True)

