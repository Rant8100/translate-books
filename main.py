import os
import time
import re
import json
from openai import OpenAI
from dotenv import load_dotenv

from prompts import PROMPT_BATCH_ANALYSIS, PROMPT_FINAL_MERGE, PROMPT_MIMIC_TRANSLATE

load_dotenv() 

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ ОШИБКА: Не найден API ключ!")
    print("1. Создайте файл .env рядом с main.py")
    print("2. Напишите внутри: OPENAI_API_KEY=sk-proj-ваш_ключ")
    exit()

client = OpenAI(api_key=api_key)

# --- НАСТРОЙКИ ---
DIRS = {
    "examples": "examples",       
    "style": "style_guide",      
    "input": "to_translate",      
    "output": "output"           
}


ANALYSIS_CHUNK_SIZE = 40000 

TRANSLATION_CHUNK_SIZE = 6000 


def read_txt(path):
    try:
        with open(path, 'r', encoding='utf-8') as f: return f.read()
    except Exception as e:
        print(f"Ошибка чтения {path}: {e}")
        return ""

def save_txt(path, content):
    with open(path, 'w', encoding='utf-8') as f: f.write(content)

def clean_json(text):
    """Чистит ответ от маркдауна ```json ... ```"""
    match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    if match: return match.group(1)
    return text.replace("```json", "").replace("```", "")

def call_llm(prompt, model="gpt-4o"):
    """
    Умная функция вызова API.
    Если ловит ошибку лимитов (Rate Limit) — ждет и пробует снова.
    """
    for attempt in range(3):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4
            )
            return resp.choices[0].message.content
        except Exception as e:
            err_msg = str(e).lower()
            print(f"⚠️ API Error ({model}, попытка {attempt+1}): {e}")
            
            if "rate_limit" in err_msg or "429" in err_msg:
                print("⏳ Лимит API превышен. Жду 20 секунд...")
                time.sleep(20)
            else:
                time.sleep(5)
    return ""

def split_text_smart(text, limit):
    """Режет текст по абзацам, не разрывая предложения."""
    paragraphs = text.split('\n')
    chunks = []
    current_chunk = []
    current_len = 0
    for p in paragraphs:

        if current_len + len(p) > limit and current_chunk:
            chunks.append("\n".join(current_chunk))
            current_chunk = []
            current_len = 0
        current_chunk.append(p)
        current_len += len(p) + 1
    if current_chunk: chunks.append("\n".join(current_chunk))
    return chunks


def perform_deep_scan():
    print("\n🕵️ НАЧИНАЮ ГЛУБОКОЕ СКАНИРОВАНИЕ ВСЕХ КНИГ...")
    
    files = sorted(os.listdir(DIRS["examples"]))
    sources = [f for f in files if "_source.txt" in f]
    
    all_notes = [] 
    full_reference_text = ""

    if not sources:
        print("❌ Нет файлов в папке examples.")
        return None, None

    total_files = len(sources)
    for idx, src in enumerate(sources):
        tgt = src.replace("_source.txt", "_target.txt")
        if tgt not in files: continue
        
        print(f"   📖 Читаю книгу {idx+1}/{total_files}: {src}...")
        
        s_text = read_txt(os.path.join(DIRS["examples"], src))
        t_text = read_txt(os.path.join(DIRS["examples"], tgt))
        
        if len(full_reference_text) < 5000:
            full_reference_text += t_text[:5000]

        s_chunks = split_text_smart(s_text, ANALYSIS_CHUNK_SIZE)
        t_chunks = split_text_smart(t_text, ANALYSIS_CHUNK_SIZE)
        
        limit = min(len(s_chunks), len(t_chunks))
        
        for i in range(limit):
            print(f"      🔬 Анализ фрагмента {i+1}/{limit}...")
            combined_chunk = f"ORIGINAL:\n{s_chunks[i]}\n\nTRANSLATION:\n{t_chunks[i]}"
            
            notes = call_llm(PROMPT_BATCH_ANALYSIS.format(content_chunk=combined_chunk), model="gpt-4o-mini")
            if notes:
                all_notes.append(notes)

    print("\n🧠 ОБЪЕДИНЯЮ ДАННЫЕ В ЕДИНЫЙ DNA...")
    
    raw_data = "\n\n=== ЗАМЕТКИ ===\n".join(all_notes)
    
    try_limits = [160000, 80000, 40000] 
    
    final_json = None
    
    for limit in try_limits:
        print(f"   🔄 Пробую собрать DNA (объем данных: {limit} симв)...")
        safe_data = raw_data[:limit]
        
        final_json_str = call_llm(PROMPT_FINAL_MERGE.format(raw_notes=safe_data), model="gpt-4o-mini")
        cleaned = clean_json(final_json_str)
        
        if cleaned and len(cleaned) > 20 and "Error" not in cleaned:
            final_json = cleaned
            break # Успех!
        else:
            print("   ⚠️ Слишком много данных. Урезаю и пробую снова...")

    if not final_json:
        print("❌ ОШИБКА: Не удалось создать DNA. Проверьте файлы примеров.")
        return None, None

    # Сохраняем результат
    dna_path = os.path.join(DIRS["style"], "translator_dna.json")
    save_txt(dna_path, final_json)
    print("✅ MASTER DNA УСПЕШНО СОЗДАН.")
    
    return final_json, full_reference_text


def main():

    for d in DIRS.values(): os.makedirs(d, exist_ok=True)
    
    dna_path = os.path.join(DIRS["style"], "translator_dna.json")
    
    if os.path.exists(dna_path):
        print("ℹ️ Найден существующий DNA.")
        choice = input("Пересоздать его заново (сканировать все книги)? (y/n): ")
        if choice.lower() == 'y':
            style_dna, ref_text = perform_deep_scan()
        else:
            style_dna = read_txt(dna_path)
            ref_text = "Текст для примера стиля..." 
    else:
        style_dna, ref_text = perform_deep_scan()

    if not style_dna: return

    input_files = [f for f in os.listdir(DIRS["input"]) if f.endswith(".txt")]
    
    if not input_files:
        print(f"📂 Папка {DIRS['input']} пуста. Положите туда .txt файл.")
        return

    for filename in input_files:
        print(f"\n🚀 ПЕРЕВОД КНИГИ: {filename}")
        full_source = read_txt(os.path.join(DIRS["input"], filename))
        chunks = split_text_smart(full_source, TRANSLATION_CHUNK_SIZE)
        
        full_translation = []
        for i, chunk in enumerate(chunks):
            print(f"   ⏳ Перевожу часть {i+1}/{len(chunks)}...")
            
            prompt = PROMPT_MIMIC_TRANSLATE.format(
                style_json=style_dna,
                reference_sample=ref_text[:2000],
                source_text=chunk
            )
            
            res = call_llm(prompt, model="gpt-4o") 
            res = clean_json(res)
            
            full_translation.append(res)
            
            save_txt(os.path.join(DIRS["output"], f"temp_{filename}"), "\n".join(full_translation))

        final_path = os.path.join(DIRS["output"], filename.replace(".txt", "_RU.txt"))
        save_txt(final_path, "\n".join(full_translation))
        print(f"🏁 ГОТОВО! Файл сохранен: {final_path}")

        if os.path.exists(os.path.join(DIRS["output"], f"temp_{filename}")):
            os.remove(os.path.join(DIRS["output"], f"temp_{filename}"))

if __name__ == "__main__":
    main()
