from views.main_view import MainView
import customtkinter as ctk


class MainController:
    def __init__(self, root, model, on_logout_callback):
        self.root = root
        self.model = model
        self.on_logout_callback = on_logout_callback

        # Створюємо головний View
        self.view = MainView(self.root, self.navigate)
        self.content_container = self.view.get_content_container()

        # Словник для зберігання наших екранів (щоб не створювати їх заново щоразу)
        self.frames = {}

        # Створюємо заглушки для екранів (потім ми замінимо їх на справжні View)
        self._init_dummy_frames()

    def show(self):
        """Показує головний екран і за замовчуванням відкриває Таймер"""
        self.view.pack(fill="both", expand=True)
        self.navigate("timer")

    def hide(self):
        """Ховає головний екран"""
        self.view.pack_forget()

    def navigate(self, destination):
        """Обробник кліків по меню"""
        if destination == "logout":
            self.model.token = None  # Очищаємо токен
            self.hide()
            self.on_logout_callback()
            return

        # Ховаємо всі екрани
        for frame in self.frames.values():
            frame.grid_remove()

        # Показуємо потрібний екран
        if destination in self.frames:
            self.frames[destination].grid(row=0, column=0, sticky="nsew")

    def _init_dummy_frames(self):
        """Тимчасові екрани, поки ми не напишемо справжні TimerView, ProjectView тощо"""
        # Таймер
        frame_timer = ctk.CTkFrame(self.content_container)
        ctk.CTkLabel(frame_timer, text="Екран Таймера (В розробці)", font=("Arial", 24)).pack(expand=True)
        self.frames["timer"] = frame_timer

        # Проєкти
        frame_projects = ctk.CTkFrame(self.content_container)
        ctk.CTkLabel(frame_projects, text="Екран Проєктів (В розробці)", font=("Arial", 24)).pack(expand=True)
        self.frames["projects"] = frame_projects

        # Аналітика
        frame_reports = ctk.CTkFrame(self.content_container)
        ctk.CTkLabel(frame_reports, text="Екран Аналітики (В розробці)", font=("Arial", 24)).pack(expand=True)
        self.frames["reports"] = frame_reports