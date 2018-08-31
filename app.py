from flask import Flask, render_template, request
import lz77_rust

app = Flask(__name__)


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


@app.route('/', methods=['GET', 'POST'])
def process_compress_request():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        params = request.form
        files = request.files
        if 'file' in files:
            file = files['file']
            text = file.read().decode('utf-8-sig')
            (compressed, decompressed), (size_before, size_after) = lz77_rust.get_results(text)
            write_to_file(decompressed, 'output.txt')
            return render_template('index.html',
                                   **get_template_params(text, compressed, decompressed, size_before, size_after))
        elif 'text_to_compress' in params:
            text = params['text_to_compress']
            (compressed, decompressed), (size_before, size_after) = lz77_rust.get_results(text)
            write_to_file(decompressed, 'output.txt')
            return render_template('index.html',
                                   **get_template_params(text, compressed, decompressed, size_before, size_after))
        elif 'compression_algorithm' in params:
            return render_template('index.html',
                                   decompressed_text=params['compression_algorithm'],)
        else:
            return "<h2>BAD REQUEST</h2>", 400


if __name__ == '__main__':
    app.run()
