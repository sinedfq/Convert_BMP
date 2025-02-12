def read_bmp(filename):
    with open(filename, 'rb') as f:
        # Чтение заголовка файла (14 байт)
        bmp_header = f.read(14)
        if bmp_header[:2] != b'BM':
            raise ValueError("Not a valid BMP file")

        # Чтение заголовка изображения (DIB header, 40 байт)
        dib_header = f.read(40)
        width = int.from_bytes(dib_header[4:8], byteorder='little')
        height = int.from_bytes(dib_header[8:12], byteorder='little')
        bits_per_pixel = int.from_bytes(dib_header[14:16], byteorder='little')

        # Если у открыто файла глубина цвета не 8 бит, то выход с ошибкой
        if bits_per_pixel != 8:
            raise ValueError("Only 8-bit BMP files are supported")

        # Чтение палитры (256 цветов, 1024 байта)
        palette = f.read(1024)  # 256 * 4 (RGBA)

        # Чтение данных пикселей, размер строки с выравниванием
        row_size = (width + 3) // 4 * 4
        pixel_data = []

        # Чтение строк изображения
        for y in range(height):
            row = f.read(row_size)
            pixel_data.append(row)

    return width, height, palette, pixel_data

# Функция по преобразованию RGB цветов к ЧБ формату
def convert_to_grayscale(palette):
    # Новый массив для палитры в оттенках серого
    gray_palette = bytearray(1024)

    # Заполнение массива серой палитры
    for i in range(256):
        r = palette[i * 4]
        g = palette[i * 4 + 1]
        b = palette[i * 4 + 2]
        gray_value = (r + g + b) // 3
        gray_palette[i * 4:i * 4 + 4] = [gray_value, gray_value, gray_value, 255]  # RGBA

    return gray_palette

# Функция записи изображения в новый файл с ЧБ форматом изображения
def write_bmp(filename, width, height, gray_palette, pixel_data):
    with open(filename, 'wb') as f:
        # Запись заголовка файла
        f.write(b'BM')
        file_size = 14 + 40 + len(gray_palette) + len(pixel_data) * (width + 3) // 4 * 4
        f.write(file_size.to_bytes(4, byteorder='little'))
        f.write((0).to_bytes(2, byteorder='little'))
        f.write((0).to_bytes(2, byteorder='little'))
        f.write((14 + 40 + len(gray_palette)).to_bytes(4, byteorder='little'))

        # Запись заголовка изображения
        f.write((40).to_bytes(4, byteorder='little'))  # DIB header size
        f.write(width.to_bytes(4, byteorder='little'))
        f.write(height.to_bytes(4, byteorder='little'))
        f.write((1).to_bytes(2, byteorder='little'))  # Planes
        f.write((8).to_bytes(2, byteorder='little'))  # Bit depth
        f.write((0).to_bytes(4, byteorder='little'))  # Compression
        f.write((0).to_bytes(4, byteorder='little'))  # Image size
        f.write((0).to_bytes(4, byteorder='little'))  # Horizontal resolution
        f.write((0).to_bytes(4, byteorder='little'))  # Vertical resolution
        f.write((256).to_bytes(4, byteorder='little'))  # Colors in palette
        f.write((0).to_bytes(4, byteorder='little'))  # Important colors

        # Запись палитры
        f.write(gray_palette)

        # Запись данных пикселей в правильном порядке: Записываем строки в том порядке, в котором они были прочитаны
        for row in pixel_data:
            f.write(row)

if __name__ == "__main__":
    input_bmp_file = "CAT256.bmp"
    output_bmp_file = "CAT256_grey.bmp"
    try:
        width, height, palette, pixel_data = read_bmp(input_bmp_file)
        gray_palette = convert_to_grayscale(palette)
        write_bmp(output_bmp_file, width, height, gray_palette, pixel_data)
        print("Conversion completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
