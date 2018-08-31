from flask import Flask, render_template, request
import lz77_rust
import huffman.huffman as huffman

app = Flask(__name__)


ALGORITHMS = {
    'lz77': lz77_rust.get_results,
    'huffman': huffman.get_results,
}


def get_template_params(text, compressed, decompressed, size_before, size_after):
    return {
        'initial_text': text,
        'compressed_text': compressed,
        'decompressed_text': decompressed,
        'size_compressed': "{} bytes".format(size_after),
        'size_decompressed': "{} bytes".format(size_before),
    }


def write_to_file(decompressed_text, output_path):
    with open(output_path, 'w', encoding='utf-8-sig') as file:
        file.write(decompressed_text)


def get_template_params_wrapper(func, text):
    (compressed, decompressed), (size_before, size_after) = func(text)
    return get_template_params(text, compressed, decompressed, size_before, size_after)


def render_process_file(file, compression_func):
    text = file.read().decode('utf-8-sig')
    template_params = get_template_params_wrapper(compression_func, text)
    write_to_file(template_params['decompressed_text'], 'output.txt')
    return render_template('index.html', **template_params)


def render_process_text(text, compression_func):
    template_params = get_template_params_wrapper(compression_func, text)
    write_to_file(template_params['decompressed_text'], 'output.txt')
    return render_template('index.html', **template_params)


@app.route('/', methods=['GET', 'POST'])
def process_compress_request():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        params = request.form
        print(params)
        files = request.files
        compression_func = ALGORITHMS[params['compression_algorithm']]

        if 'file' in files:
            return render_process_file(files['file'], compression_func)

        elif 'text_to_compress' in params:
            return render_process_text(params['text_to_compress'], compression_func)

        else:
            return "<h2>BAD REQUEST</h2>", 400


if __name__ == '__main__':
    app.run()
