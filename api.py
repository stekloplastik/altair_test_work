import requests
import xml.etree.ElementTree as ET


REMOTE_FEED_URL = 'https://stripmag.ru/datafeed/p5s_full_stock.xml'
OUR_FEED_URL = 'http://alitair.1gb.ru/Intim_Ali_allfids_2.xml'
SAVING_PATH = ''


def download_file_from_url(url, file):
    """Загружаем файлы по ссылкам"""

    if type(url) != str:
        raise TypeError(f'Argument <url> must be str, not {type(url)}')

    if type(file) != str:
        raise TypeError(f'Argument <file> must be str, not {type(file)}')

    response = requests.get(url)
    with open(file, 'wb') as f_out:
        f_out.write(response.content)


def update_feed(source, target):
    """Обновляем все данные в целевом файле из исходного"""

    # Получаем дерево исходного файла
    s_tree = ET.parse(source)
    s_root = s_tree.getroot()
    s_products = s_root.findall('product')
    print('Получены данные из исходного файла')

    # Получаем дерево целевого файла
    t_tree = ET.parse(target)
    t_root = t_tree.getroot()
    t_offers = t_root.find('shop').find('offers')
    print('Получены данные из целевого файла')

    for item in s_products:

        id = item.get('prodID')
        offer = t_offers.find(f'offer[@id="{id}"]')
        if offer is None:
            continue

        s_price = item.find('price')
        s_count = item.find('assortiment').find('assort')

        t_price = offer.find('price')
        t_count = offer.find('quantity')

        # Меняем количество
        t_count.text = s_count.get('sklad')

        # Меняем цену
        t_price.set('BaseRetailPrice', s_price.get('BaseRetailPrice'))
        t_price.set('BaseWholePrice', s_price.get('BaseWholePrice'))
        t_price.set('RetailPrice', s_price.get('RetailPrice'))
        t_price.set('WholePrice', s_price.get('WholePrice'))

    print('Все успешно обработано')
    t_tree.write(target)
    print(f'Файл сохранен как: {target}')


def get_filename_from_url(url):
    """Получаем имя файла из URL"""

    if type(url) != str:
        raise TypeError(f'Argument <url> must be str, not {type(url)}')
    return url[url.rfind('/') + 1:]


if __name__ == '__main__':

    # Получаем имена файлов из URL
    remote_file = f'{SAVING_PATH}{get_filename_from_url(REMOTE_FEED_URL)}'
    our_file = f'{SAVING_PATH}{get_filename_from_url(OUR_FEED_URL)}'

    # Загружаем файлы
    download_file_from_url(REMOTE_FEED_URL, remote_file)
    download_file_from_url(OUR_FEED_URL, our_file)

    # Обновляем и сохраняем файлы
    update_feed(remote_file, our_file)