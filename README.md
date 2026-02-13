📚 AI Book Translator (Style Clone)
This project is not just a simple auto-translator. It is an intelligent style clone that reads your previous translations (or books from a specific publisher), compiles a "Style DNA" (glossary of names, speech patterns, rhythm), and translates a new book while mimicking this exact style.

It leverages the OpenAI API (combining the cost-effective gpt-4o-mini for deep analysis and the powerful gpt-4o for high-quality literary translation).

✨ Features
🕵️ Deep Scan: Reads up to 4 full books to build a unified glossary of names and terms.

🧠 Style Cloning: Mimics the syntax, vocabulary, and tone of the original translator/author.

💰 Cost-Efficient: Uses the cheaper model for analyzing millions of characters, and the premium model only for the final translation.

🛡️ Secure: Works via .env, keeping your API keys safe from the code.

🧱 Smart Splitting: Handles large texts without breaking paragraphs or sentences.

🔄 Auto-Retry: Automatically pauses and retries if API rate limits are reached.

🚀 Installation
1. Requirements
Python 3.8+

OpenAI Account with an API Key

2. Download
Clone the repository:

Bash
git clone https://github.com/Rant8100/translate-books.git
cd translate-books
3. Install Dependencies
Install the required packages:

Bash
pip install openai python-dotenv
⚙️ Configuration (Important!)
Create a file named .env in the root folder of the project.

Add your OpenAI API Key inside:

Code snippet
OPENAI_API_KEY=sk-proj-your_long_key_here
Warning: Never add the .env file to Git! The project includes a .gitignore file to prevent this.

📖 How to Use
Step 1. Training (The examples folder)
Place your high-quality translation examples in the examples/ folder. These must be pairs of .txt files:

book1_source.txt (Original English text)

book1_target.txt (Russian translation)

book2_source.txt

book2_target.txt

The more examples you provide, the better the bot learns names and style.

Step 2. Input Book (The to_translate folder)
Place the single .txt file of the book you want to translate into the to_translate/ folder.
Example: new_book.txt.

Step 3. Run
Execute the script:

Bash
python main.py
The Process:
Scanning Phase: The bot reads all books in examples. This may take 5-15 minutes.

DNA Phase: The bot creates a style_guide/translator_dna.json file containing the glossary and style rules.

Translation Phase: The bot begins translating the book in to_translate. Results appear in the output folder.

📱 How to Create a Beautiful E-book (EPUB/FB2)
The bot outputs a _RU.txt file containing HTML tags (italics, bold text). To read this comfortably on a phone or Kindle:

Download Calibre.

Rename your translation file: Change extension from .txt to .html (e.g., book_RU.html).

Drag and drop the file into Calibre.

Click "Convert books".

Styling Settings:

Look & Feel -> Layout: Check "Remove spacing between paragraphs".

Indent: Set "Indent size" to 1.5 em.

Select output format: EPUB (for iPhone/Android) or AZW3 (for Kindle).

Click OK.

📂 Project Structure
Plaintext
translation_project/
├── .env                  # INSERT KEY HERE (Secret!)
├── .gitignore            # List of ignored files
├── main.py               # Main logic script
├── prompts.py            # AI Instructions
├── style_guide/          # Stores the "Style DNA" (JSON)
├── examples/             # Place training pairs here (.txt)
│   ├── b1_source.txt
│   └── b1_target.txt
├── to_translate/         # Place the book to translate here
│   └── my_book.txt
└── output/               # Finished translations appear here
⚠️ Limits & Costs
Analysis: Uses gpt-4o-mini. Very cheap, even for multiple books.

Translation: Uses gpt-4o. More expensive, but provides literary quality.

Estimated Cost: Approximately $2 - $6 per average-sized book (depending on length).





📚 AI Book Translator (Style Clone)
Этот проект — не просто автопереводчик. Это умный бот-клон, который сначала читает ваши предыдущие переводы (или книги любимого издательства), составляет "ДНК стиля" (глоссарий имен, манера речи, ритм) и переводит новую книгу, подражая этому стилю.

Использует OpenAI API (связку дешевой модели gpt-4o-mini для анализа и мощной gpt-4o для художественного перевода).

✨ Возможности
🕵️ Глубокий анализ (Deep Scan): Читает до 4-х книг целиком, чтобы составить единый глоссарий имен и терминов.

🧠 Клонирование стиля: Копирует синтаксис, лексику и тон автора/переводчика.

💰 Экономия: Использует дешевую модель для анализа миллионов символов, а дорогую — только для финального перевода.

🛡️ Безопасность: Работает через .env, ключи не попадают в код.

🧱 Умная нарезка: Не разрывает абзацы и предложения при переводе.

🔄 Авто-повтор: Если API перегружен, бот сам подождет и продолжит работу.

🚀 Установка
1. Требования
Python 3.8+

Аккаунт OpenAI с API ключом

2. Скачивание
Клонируйте репозиторий:

Bash
git clone https://github.com/Rant8100/translate-books.git
cd translate-books
3. Библиотеки
Установите необходимые пакеты:

Bash
pip install openai python-dotenv
⚙️ Настройка (Важно!)
Создайте в корне проекта файл с именем .env.

Вставьте туда свой ключ OpenAI:

Code snippet
OPENAI_API_KEY=sk-proj-ваш_длинный_ключ_здесь
Внимание: Никогда не добавляйте файл .env в Git! Для этого в проекте есть .gitignore.

📖 Как пользоваться
Шаг 1. Обучение (Папка examples)
Положите в папку examples/ примеры качественного перевода. Это должны быть пары текстовых файлов .txt:

book1_source.txt (Оригинал на английском)

book1_target.txt (Перевод на русском)

book2_source.txt

book2_target.txt

Чем больше примеров, тем точнее бот выучит имена героев и стиль.

Шаг 2. Книга для перевода (Папка to_translate)
Положите один файл .txt с книгой, которую хотите перевести, в папку to_translate/.
Например: new_book.txt.

Шаг 3. Запуск
Запустите скрипт:

Bash
python main.py
Процесс работы:
Фаза сканирования: Бот прочитает все книги из examples. Это может занять 5-15 минут.

Фаза DNA: Бот создаст файл style_guide/translator_dna.json с глоссарием и правилами.

Фаза перевода: Бот начнет переводить книгу из to_translate. Результат будет появляться в папке output.

📱 Как сделать красивую книгу (EPUB/FB2)
Бот выдает файл _RU.txt с HTML-тегами (курсив, жирный шрифт). Чтобы читать его на телефоне или Kindle:

Скачайте программу Calibre.

Переименуйте файл перевода: .txt -> .html (например, book_RU.html).

Закиньте файл в Calibre.

Нажмите "Преобразовать" (Convert).

Настройки для красоты:

Внешний вид -> Макет: Поставьте галочку "Удалить интервалы между абзацами".

Отступ: Установите "1.5 em".

Сохраните как EPUB (для iPhone/Android) или AZW3 (для Kindle).

📂 Структура проекта
Plaintext
translation_project/
├── .env                  # СЮДА ВСТАВЛЯТЬ КЛЮЧ (Секретно!)
├── .gitignore            # Список игнорируемых файлов
├── main.py               # Основной код
├── prompts.py            # Инструкции для AI
├── style_guide/          # Сюда сохраняется "ДНК" стиля (JSON)
├── examples/             # Сюда кладем пары txt для обучения
│   ├── b1_source.txt
│   └── b1_target.txt
├── to_translate/         # Сюда кладем книгу для перевода
│   └── my_book.txt
└── output/               # Здесь появится готовый перевод
⚠️ Лимиты и стоимость
Анализ: Использует gpt-4o-mini. Это очень дешево, даже для 4-х книг.

Перевод: Использует gpt-4o. Это дороже, но дает литературное качество.

Примерная стоимость перевода книги среднего размера: $2 - $6 (зависит от объема).
