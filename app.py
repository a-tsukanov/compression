from flask import Flask, render_template, request
from controllers.compression import render_compress_file, render_compress_text, ALGORITHMS
from controllers.encryption import render_encrypt_file, render_encrypt_text

app = Flask(__name__)


@app.route('/', methods=['GET'])
def show_main_page():
    return render_template('index.html')


@app.route('/compression/', methods=['GET', 'POST'])
def process_compress_request():
    if request.method == 'GET':
        return render_template('compression.html')

    elif request.method == 'POST':
        params = request.form
        print(params)
        files = request.files
        compression_func = ALGORITHMS[params['compression_algorithm']]

        if 'file' in files:
            return render_compress_file(files['file'], compression_func)

        elif 'text_to_compress' in params:
            return render_compress_text(params['text_to_compress'], compression_func)

        else:
            return "<h2>BAD REQUEST</h2>", 400


@app.route('/rsa/', methods=['GET', 'POST'])
def process_rsa_request():
    if request.method == 'GET':
        return render_template('rsa.html')

    elif request.method == 'POST':
        params = request.form
        print(params)
        files = request.files
        numeric_params = params['p'], params['q'], params['e']

        if 'file' in files:
            return render_encrypt_file(files['file'], numeric_params)

        elif 'text_to_compress' in params:
            return render_encrypt_text(params['text_to_compress'], numeric_params)

        else:
            return "<h2>BAD REQUEST</h2>", 400


@app.route('/zero_knowledge_proof/', methods=['GET', 'POST'])
def process_fiat_shamir_request():
    if request.method == 'GET':
        return render_template('fiat_shamir.html')

    elif request.method == 'POST':
        raise NotImplementedError


if __name__ == '__main__':
    app.run()
