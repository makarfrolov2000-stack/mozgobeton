import pygame
import sys
import os
import re
from System.Мозг.settings import *
from System.Сердце.questions import SUBJECTS, SUBJECTS_DATA


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()

        self.font_big = pygame.font.SysFont("arial", 40, bold=True)
        self.font_mid = pygame.font.SysFont("arial", 24)
        self.font_small = pygame.font.SysFont("arial", 18)
        self.font_hand = pygame.font.SysFont("comicsansms", 32)

        self.state = "MENU"
        self.score = 0

        # НОВОЕ: текущий выбранный предмет
        self.current_subject = ""

        self.board_pages = []
        self.board_page = 0

        self.q_index = 0
        self.first_try = True
        self.user_input = ""
        self.feedback_msg = ""
        self.feedback_color = NOTEBOOK_TEXT
        self.feedback_timer = 0.0
        self.answer_is_correct = False

        self.bg_image = None
        try:
            path = os.path.join("Сердце", "background.jpg")
            self.bg_image = pygame.image.load(path)
            self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH, HEIGHT))
        except:
            pass

        self._create_buttons()

    def _create_buttons(self):
        self.btn_play = pygame.Rect(WIDTH // 2 - 150, 300, 300, 60)
        self.btn_shop = pygame.Rect(WIDTH // 2 - 150, 380, 300, 60)

        self.btn_subjects = []
        for i in range(len(SUBJECTS)):
            self.btn_subjects.append(pygame.Rect(WIDTH // 2 - 200, 180 + i * 80, 400, 60))

        self.btn_lesson1 = pygame.Rect(WIDTH // 2 - 200, 300, 400, 80)

        self.btn_arrow_left = pygame.Rect(50, HEIGHT - 80, 150, 50)
        self.btn_arrow_right = pygame.Rect(WIDTH - 200, HEIGHT - 80, 150, 50)
        self.btn_to_notebook = pygame.Rect(WIDTH // 2 - 150, HEIGHT - 80, 300, 50)

        self.input_rect = pygame.Rect(WIDTH // 2 - 200, 300, 400, 60)
        self.btn_check = pygame.Rect(WIDTH // 2 - 100, 400, 200, 50)

        self.btn_back_menu = pygame.Rect(20, 20, 100, 40)

    def draw_text_center(self, text, font, color, y):
        surf = font.render(text, True, color)
        self.screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, y))

    def paginate_text(self, text, font, max_width, max_height):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())

        pages = []
        lines_per_page = max_height // 35
        for i in range(0, len(lines), lines_per_page):
            pages.append(lines[i:i + lines_per_page])
        return pages

    def draw_menu(self):
        self.screen.fill(BG)
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
        else:
            self.screen.fill(BG)

        self.draw_text_center("МОЗГОБЕТОН", self.font_big, ACCENT, 150)

        pygame.draw.rect(self.screen, ACCENT, self.btn_play, border_radius=10)
        self.draw_text_center("ИГРАТЬ", self.font_mid, BG, self.btn_play.y + 15)

        pygame.draw.rect(self.screen, MUTED, self.btn_shop, border_radius=10)
        self.draw_text_center("МАГАЗИН (В РАЗРАБОТКЕ)", self.font_small, BG, self.btn_shop.y + 20)

    def draw_subjects(self):
        self.screen.fill(BG)
        self.draw_text_center("Выбери кабинет", self.font_big, TEXT, 80)

        for i, rect in enumerate(self.btn_subjects):
            pygame.draw.rect(self.screen, PANEL, rect, border_radius=10)
            pygame.draw.rect(self.screen, ACCENT, rect, 2, border_radius=10)
            self.draw_text_center(SUBJECTS[i], self.font_mid, TEXT, rect.y + 15)

        pygame.draw.rect(self.screen, PANEL, self.btn_back_menu, border_radius=5)
        self.draw_text_center("Назад", self.font_small, TEXT, self.btn_back_menu.y + 10)

    def draw_lessons(self):
        self.screen.fill(BG)
        self.draw_text_center(f"Урок: {self.current_subject}", self.font_big, TEXT, 100)

        pygame.draw.rect(self.screen, PANEL, self.btn_lesson1, border_radius=10)
        pygame.draw.rect(self.screen, ACCENT, self.btn_lesson1, 3, border_radius=10)
        # Показываем название темы из базы данных
        title = SUBJECTS_DATA[self.current_subject]["title"]
        self.draw_text_center(title, self.font_mid, TEXT, self.btn_lesson1.y + 25)

        pygame.draw.rect(self.screen, PANEL, self.btn_back_menu, border_radius=5)
        self.draw_text_center("Назад", self.font_small, TEXT, self.btn_back_menu.y + 10)

    def draw_board(self):
        self.screen.fill((80, 60, 50))
        pygame.draw.rect(self.screen, DESK_BG, (0, HEIGHT - 120, WIDTH, 120))

        board_rect = pygame.Rect(100, 50, WIDTH - 200, HEIGHT - 200)
        pygame.draw.rect(self.screen, (139, 69, 19), board_rect)
        pygame.draw.rect(self.screen, BOARD_BG, board_rect.inflate(-20, -20))

        if self.board_page < len(self.board_pages):
            page_lines = self.board_pages[self.board_page]
            y_offset = 80
            for line in page_lines:
                surf = self.font_mid.render(line, True, BOARD_TEXT)
                self.screen.blit(surf, (130, y_offset))
                y_offset += 35

        if self.board_page > 0:
            pygame.draw.rect(self.screen, ACCENT, self.btn_arrow_left, border_radius=10)
            self.draw_text_center("< Назад", self.font_mid, BG, self.btn_arrow_left.y + 10)

        if self.board_page < len(self.board_pages) - 1:
            pygame.draw.rect(self.screen, ACCENT, self.btn_arrow_right, border_radius=10)
            self.draw_text_center("Далее >", self.font_mid, BG, self.btn_arrow_right.y + 10)
        else:
            pygame.draw.rect(self.screen, CORRECT, self.btn_to_notebook, border_radius=10)
            self.draw_text_center("Открыть тетрадь", self.font_mid, BG, self.btn_to_notebook.y + 10)

    def draw_quiz(self):
        self.screen.fill((100, 120, 140))
        nb_rect = pygame.Rect(100, 50, WIDTH - 200, HEIGHT - 100)
        pygame.draw.rect(self.screen, NOTEBOOK_BG, nb_rect, border_radius=5)

        for i in range(10, HEIGHT - 100, 40):
            pygame.draw.line(self.screen, NOTEBOOK_LINES, (110, 50 + i), (WIDTH - 110, 50 + i), 1)

        score_txt = self.font_mid.render(f"Очки: {self.score}", True, NOTEBOOK_TEXT)
        self.screen.blit(score_txt, (WIDTH - 150, 20))

        # Получаем вопрос из текущего предмета
        questions = SUBJECTS_DATA[self.current_subject]["questions"]
        q = questions[self.q_index]

        self.draw_text_center(f"Задание {self.q_index + 1} из {len(questions)}:", self.font_mid, NOTEBOOK_TEXT, 80)

        words = q["q"].split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if self.font_mid.size(test_line)[0] <= WIDTH - 250:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())

        y_offset = 120
        for line in lines:
            self.draw_text_center(line, self.font_mid, NOTEBOOK_TEXT, y_offset)
            y_offset += 30

        self.input_rect.y = y_offset + 30
        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect, border_radius=5)
        pygame.draw.rect(self.screen, NOTEBOOK_TEXT, self.input_rect, 2, border_radius=5)

        cursor = "|" if pygame.time.get_ticks() % 1000 < 500 else ""
        display_text = self.user_input + cursor
        txt_surf = self.font_hand.render(display_text, True, NOTEBOOK_TEXT)
        self.screen.blit(txt_surf, (self.input_rect.x + 15, self.input_rect.y + 10))

        self.btn_check.y = self.input_rect.y + 80
        pygame.draw.rect(self.screen, ACCENT, self.btn_check, border_radius=8)
        self.draw_text_center("Проверить (Enter)", self.font_mid, BG, self.btn_check.y + 12)

        if self.feedback_msg:
            self.draw_text_center(self.feedback_msg, self.font_big, self.feedback_color, self.btn_check.y + 70)

    def check_answer(self):
        if not self.user_input.strip(): return

        questions = SUBJECTS_DATA[self.current_subject]["questions"]
        q = questions[self.q_index]

        user_words = re.sub(r'[^\w\s]', ' ', self.user_input).split()
        correct_words = [re.sub(r'[^\w\s]', '', str(ans)).strip() for ans in q["answer"]]

        if sorted(user_words) == sorted(correct_words):
            self.feedback_msg = "ВЕРНО! ✅"
            self.feedback_color = CORRECT
            self.answer_is_correct = True
            if self.first_try:
                self.score += 1
            self.feedback_timer = 1.0
        else:
            self.feedback_msg = "ОШИБКА! ❌"
            self.feedback_color = WRONG
            self.answer_is_correct = False
            if self.first_try:
                self.score -= 1
                self.first_try = False
            self.feedback_timer = 1.5
            self.user_input = ""

    def handle_click(self, pos):
        if self.state == "MENU":
            if self.btn_play.collidepoint(pos): self.state = "SUBJECTS"

        elif self.state == "SUBJECTS":
            if self.btn_back_menu.collidepoint(pos):
                self.state = "MENU"
            else:
                for i, rect in enumerate(self.btn_subjects):
                    if rect.collidepoint(pos):
                        self.current_subject = SUBJECTS[i]
                        self.state = "LESSONS"
                        break

        elif self.state == "LESSONS":
            if self.btn_lesson1.collidepoint(pos):
                self.state = "BOARD"
                self.board_page = 0
                # Загружаем теорию для нужного предмета
                theory_text = SUBJECTS_DATA[self.current_subject]["theory"]
                self.board_pages = self.paginate_text(theory_text, self.font_mid, WIDTH - 280, HEIGHT - 260)
            elif self.btn_back_menu.collidepoint(pos):
                self.state = "SUBJECTS"

        elif self.state == "BOARD":
            if self.board_page > 0 and self.btn_arrow_left.collidepoint(pos):
                self.board_page -= 1
            elif self.board_page < len(self.board_pages) - 1 and self.btn_arrow_right.collidepoint(pos):
                self.board_page += 1
            elif self.board_page == len(self.board_pages) - 1 and self.btn_to_notebook.collidepoint(pos):
                self.state = "QUIZ"
                self.q_index = 0
                self.first_try = True
                self.user_input = ""
                self.feedback_msg = ""

        elif self.state == "QUIZ":
            if self.feedback_timer <= 0:
                if self.btn_check.collidepoint(pos):
                    self.check_answer()

    def next_question(self):
        self.user_input = ""
        self.feedback_msg = ""
        questions = SUBJECTS_DATA[self.current_subject]["questions"]
        if self.q_index < len(questions) - 1:
            self.q_index += 1
            self.first_try = True
        else:
            self.state = "MENU"
            self.score = 0

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)

                elif event.type == pygame.KEYDOWN and self.state == "QUIZ":
                    if self.feedback_timer <= 0:
                        if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                            self.check_answer()
                        elif event.key == pygame.K_BACKSPACE:
                            self.user_input = self.user_input[:-1]
                        elif event.unicode.isprintable() and len(self.user_input) < 25:
                            self.user_input += event.unicode

            if self.state == "MENU":
                self.draw_menu()
            elif self.state == "SUBJECTS":
                self.draw_subjects()
            elif self.state == "LESSONS":
                self.draw_lessons()
            elif self.state == "BOARD":
                self.draw_board()
            elif self.state == "QUIZ":
                self.draw_quiz()

                if self.feedback_timer > 0:
                    self.feedback_timer -= dt
                    if self.feedback_timer <= 0:
                        if self.answer_is_correct:
                            self.next_question()
                        else:
                            self.feedback_msg = ""

            pygame.display.flip()
        pygame.quit()
        sys.exit()