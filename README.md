<H2>Преобразователь 8-битного BMP RGB файла в ЧБ-формат </H2>

<h3>Задание: </h3>

1. Преобразовать цветной BMP файл с глубиной цвета 8 бит в BMP файл
в оттенках серого (найти в файле палитру, преобразовать ее, усреднив по
тройкам RGB цветов и записать получившийся файл под новым именем)
2. Вывести основные характеристики BMP изображения (Работа с заголовком и
палитрой).

-----

<h3>Описание основных блоков кода: </h3>

Считывание данных из BMP файла (```read_bmp```):

```python
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
```

В данной функции происходит считывание данных из BMP файла и запись их в необходимые переменные.
<br>

-----
Конвертация RGB цветов к ЧБ-формату(```convert_to_grayscal```):
```python
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

```

В данной функции RGB цвета преобразуются к ЧБ-формату, создавая новый массив ```gray_palette```

-----

Запись нового файла с преобразованием цветов в оттенки серого (```write_bmp```):

```python
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

```

В данном методе происходит запись нового файла ```CAT256_grey.bmp``` уже с новой палитрой (оттенки серого).
<br>Вначале записывается заголовок файла с указанием нужных параметров (формат изображения, общий размер файла и т.д):

```python

        f.write(b'BM')
        file_size = 14 + 40 + len(gray_palette) + len(pixel_data) * (width + 3) // 4 * 4
        f.write(file_size.to_bytes(4, byteorder='little'))
        f.write((0).to_bytes(2, byteorder='little'))
        f.write((0).to_bytes(2, byteorder='little'))
        f.write((14 + 40 + len(gray_palette)).to_bytes(4, byteorder='little'))

```

Далее происходить запись самого изображения с указанием неробходимых параметров(глубина цвета, размер изображение, сжатие и т.д.):
```python
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
```
-----

<h3>Результат работы: </h3>

![image](https://github.com/user-attachments/assets/74147e28-e0f1-4f87-86f7-ba5e37b8f706)
