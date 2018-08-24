from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def process_compress_request():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        params = request.form
        print(params)
        if 'text_to_compress' in params:
            return render_template('index.html',
                                   initial_text=params['text_to_compress'],
                                   decompressed_text=params['text_to_compress'],)
        elif 'text_to_decompress' in params:
            return render_template('index.html',
                                   compressed_text=params['text_to_decompress'],
                                   decompressed_text='lalala',)
        elif 'compression_algorithm' in params:
            return render_template('index.html',
                                   decompressed_text=params['compression_algorithm'],)
        else:
            return "<h2>BAD REQUEST</h2>", 400


if __name__ == '__main__':
    app.run()
