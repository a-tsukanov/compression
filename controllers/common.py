def write_to_file(data, output_path):
    with open(output_path, 'w', encoding='utf-8-sig') as file:
        file.write(data)