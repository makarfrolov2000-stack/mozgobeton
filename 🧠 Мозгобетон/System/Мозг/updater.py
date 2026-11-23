import urllib.request
import os


def check_for_updates():
    # ВАЖНО: Сюда вставь ссылку на свой файл в интернете (пока оставим пустую)
    # Например: "https://raw.githubusercontent.com/твой_ник/репозиторий/main/questions.py"
    UPDATE_URL = ""

    local_file = os.path.join("System", "Сердце", "questions.py")

    if not UPDATE_URL:
        print("Ссылка на обновление не указана. Играем в локальную версию.")
        return

    try:
        print("Проверяем обновления в интернете...")
        # Скачиваем файл по ссылке (ждем не больше 3 секунд)
        response = urllib.request.urlopen(UPDATE_URL, timeout=3)
        new_code = response.read().decode('utf-8')

        # Если файл уже есть, проверяем, отличается ли он от нового
        if os.path.exists(local_file):
            with open(local_file, "r", encoding="utf-8") as f:
                current_code = f.read()
            if current_code == new_code:
                print("Обновлений нет. У тебя самая свежая версия!")
                return

        # Если отличается или файла нет — перезаписываем!
        with open(local_file, "w", encoding="utf-8") as f:
            f.write(new_code)
        print("🎉 Игра успешно обновилась из интернета!")

    except Exception as e:
        print("Не удалось проверить обновления (нет интернета или ссылка не работает).")
        print("Запускаем ту версию, которая есть на компьютере.")