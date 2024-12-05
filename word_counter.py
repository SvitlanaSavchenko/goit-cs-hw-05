import requests
import re
import matplotlib.pyplot as plt

def get_file_from_url(file_url):
    """Завантажити текстовий файл з заданого URL."""
    try:
        response = requests.get(file_url)
        response.raise_for_status()  # Перевірка на успішність запиту
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Помилка при завантаженні файлу: {e}")
        return None

def map_function(text):
    """Підготовка слів з тексту для MapReduce."""
    words = re.findall(r'\b\w+\b', text.lower())  # Знаходимо всі слова
    return [(word, 1) for word in words]  # Повертаємо список кортежів (слово, 1)

def shuffle_and_sort(mapped_values):
    """Групування слів за їх частотою."""
    word_dict = {}
    for word, count in mapped_values:
        word_dict[word] = word_dict.get(word, 0) + count  # Підсумовуємо частоти
    return sorted(word_dict.items(), key=lambda x: x[1], reverse=True)  # Сортуємо за частотою

def reduce_function(text):
    """Застосування MapReduce для обробки частоти слів."""
    mapped_values = map_function(text)  # Отримуємо маповані значення
    return shuffle_and_sort(mapped_values)  # Групуємо і сортуємо

def visualize_top_words(word_frequencies, top_n=10):
    """Візуалізація топових слів з їх частотою."""
    top_words = word_frequencies[:top_n]  # Вибираємо топ N слів
    words, frequencies = zip(*top_words)  # Розпаковуємо список на два окремих списки

    plt.figure(figsize=(12, 6))
    plt.bar(words, frequencies)
    plt.title('Топ 10 слів за частотою')
    plt.xlabel('Слова')
    plt.ylabel('Частота')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    # Оновлений URL для завантаження тексту з публічного репозиторію GitHub
    url = 'https://raw.githubusercontent.com/ryanmcdermott/clean-code-javascript/master/README.md'  # Публічний текстовий файл
    
    # Завантажуємо текст
    text = get_file_from_url(url)
    if not text:
        return

    # Застосовуємо MapReduce для аналізу частоти слів
    word_frequencies = reduce_function(text)
    
    # Візуалізуємо топ-10 слів
    visualize_top_words(word_frequencies)

if __name__ == "__main__":
    main()
