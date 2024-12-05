import argparse
import asyncio
import os
import shutil
import logging

# Функція для створення тестових файлів
def create_test_files(source_folder):
    """Створення тестових файлів у папці source_folder."""
    test_files = [
        'file1.txt', 'file2.txt', 'file3.txt', 'file4.txt', 'file5.txt',
        'file1.jpg', 'file2.jpg', 'file3.jpg', 'file4.jpg', 'file5.jpg',
        'file1.pdf', 'file2.pdf',
        'file1.py', 'file2.py',
        'file1.csv', 'file2.csv',
        'file1.zip', 'file2.zip'
    ]
    os.makedirs(source_folder, exist_ok=True)

    for file in test_files:
        # Вказуємо кодування utf-8 при відкритті файлів
        with open(os.path.join(source_folder, file), 'w', encoding='utf-8') as f:
            f.write(f"Це тестовий файл: {file}")

    logging.info(f"Тестові файли створено в {source_folder}")

# Асинхронна функція для читання файлів з папки
async def read_folder(source_path):
    """Рекурсивно читає всі файли в папці source_path."""
    files = []
    for root, _, filenames in os.walk(source_path):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

# Асинхронна функція для копіювання файлів в цільову папку на основі розширення
async def copy_file(file_path, destination_path):
    """Копіює файл в папку, згруповану за розширенням."""
    try:
        file_extension = os.path.splitext(file_path)[1][1:]
        extension_folder = os.path.join(destination_path, file_extension)
        os.makedirs(extension_folder, exist_ok=True)
        destination_file = os.path.join(extension_folder, os.path.basename(file_path))
        shutil.copy2(file_path, destination_file)
        logging.info(f"Файл {file_path} скопійовано до {destination_file}")
    except Exception as e:
        logging.error(f"Помилка при обробці {file_path}: {e}")

# Основна функція для виконання асинхронного сортування файлів
async def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

    parser = argparse.ArgumentParser(description='Async File Sorter')
    parser.add_argument('source_folder', help='Шлях до вихідної папки')
    parser.add_argument('destination_folder', help='Шлях до цільової папки')

    args = parser.parse_args()

    if not os.path.exists(args.source_folder):
        create_test_files(args.source_folder)  # Якщо папка не існує, створюємо тестові файли

    os.makedirs(args.destination_folder, exist_ok=True)
    
    files = await read_folder(args.source_folder)
    await asyncio.gather(*[copy_file(file, args.destination_folder) for file in files])

if __name__ == "__main__":
    asyncio.run(main())  # Запуск асинхронної функції
