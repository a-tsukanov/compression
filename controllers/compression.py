from flask import render_template
import lz77_rust
import huffman.huffman as huffman


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


def render_compress_file(file, compression_func):
    text = file.read().decode('utf-8-sig')
    template_params = get_template_params_wrapper(compression_func, text)
    write_to_file(template_params['decompressed_text'], 'output.txt')
    return render_template('compression.html', **template_params)


def render_compress_text(text, compression_func):
    template_params = get_template_params_wrapper(compression_func, text)
    write_to_file(template_params['decompressed_text'], 'output.txt')
    return render_template('compression.html', **template_params)