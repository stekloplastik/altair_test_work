from PIL import Image


def process_images(source, form):
    """Склеиваем изображения"""


    source_img = Image.open(source)
    form_img = Image.open(form)

    # Получаем размер изображений
    source_w, source_h = source_img.size
    form_w, form_h = form_img.size

    # Вычисляем итоговый размер
    result_w = form_w if form_w > source_w else source_w
    result_h = form_h + source_h

    # Создаем новую картинку
    result_i = Image.new('RGB', (result_w, result_h))

    # Заполняем белым цветом
    result_i.paste((255, 255, 255), [0, 0, result_w, result_h])

    # вставляем изображения
    result_i.paste(source_img, ((result_w - source_w) // 2, form_h))
    result_i.paste(form_img, ((result_w - form_w) // 2, 0))

    # Сохраняем резултат
    result_i.save('result.jpg', quality=100)


if __name__ == '__main__':
    source = input('Введите путь до основного изображения: ')
    form = input('Введите путь до плашки: ')
    process_images(source, form)