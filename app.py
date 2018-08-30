from flask import Flask, render_template, request
import lz77_rust

app = Flask(__name__)


def get_template_params(text: str):
    (compressed, decompressed), (size_before, size_after) = lz77_rust.get_results(text)
    return {
        'initial_text': text,
        'compressed_text': compressed,
        'decompressed_text': decompressed,
        'size_compressed': "{} bytes".format(size_after),
        'size_decompressed': "{} bytes".format(size_before),
    }


@app.route('/', methods=['GET', 'POST'])
def process_compress_request():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        params = request.form
        print(params)
        if 'text_to_compress' in params:
            return render_template('index.html',
                                   **get_template_params(params['text_to_compress']))
        elif 'compression_algorithm' in params:
            return render_template('index.html',
                                   decompressed_text=params['compression_algorithm'],)
        else:
            return "<h2>BAD REQUEST</h2>", 400


if __name__ == '__main__':
    app.run()
