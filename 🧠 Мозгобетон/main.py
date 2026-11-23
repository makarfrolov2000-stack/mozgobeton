from System.Мозг.updater import check_for_updates
from System.Мозг.game import Game

if __name__ == "__main__":
    print("Запускаем Мозгобетон...")

    # 1. Сначала проверяем обновления в интернете
    check_for_updates()

    # 2. Затем запускаем игру
    Game().run()