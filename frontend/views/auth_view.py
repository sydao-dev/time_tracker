import customtkinter as ctk
import tkinter as tk


class AuthView(ctk.CTkFrame):
    def __init__(self, parent, login_callback):
        super().__init__(parent)
        self.login_callback = login_callback  # Зберігаємо функцію, яку передав Controller

        # Tkinter змінні (дозволяють автоматично оновлювати UI та читати дані)
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.error_var = tk.StringVar()

        # Відслідковуємо зміни: якщо користувач почав вводити текст, очищаємо помилку
        self.email_var.trace_add("write", self.clear_error)
        self.password_var.trace_add("write", self.clear_error)

        self._build_ui()

    def _build_ui(self):
        # Налаштування сітки центрування
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 5), weight=1)

        # Заголовок
        title_label = ctk.CTkLabel(self, text="Time Tracker", font=ctk.CTkFont(size=28, weight="bold"))
        title_label.grid(row=1, column=0, pady=(0, 30))

        # Поле Email
        self.email_entry = ctk.CTkEntry(
            self,
            placeholder_text="Email",
            textvariable=self.email_var,
            width=250,
            height=40
        )
        self.email_entry.grid(row=2, column=0, pady=10)
        self.email_entry.focus_set()  # Одразу ставимо курсор сюди

        # Поле Пароль
        self.password_entry = ctk.CTkEntry(
            self,
            placeholder_text="Пароль",
            show="*",
            textvariable=self.password_var,
            width=250,
            height=40
        )
        self.password_entry.grid(row=3, column=0, pady=10)

        # Прив'язка клавіші Enter до поля паролю
        self.password_entry.bind("<Return>", lambda event: self.on_login_click())

        # Кнопка входу
        self.login_btn = ctk.CTkButton(
            self,
            text="Увійти",
            command=self.on_login_click,
            width=250,
            height=40,
            font=ctk.CTkFont(weight="bold")
        )
        self.login_btn.grid(row=4, column=0, pady=20)

        # Лейбл для помилок (червоний, динамічний)
        error_label = ctk.CTkLabel(self, textvariable=self.error_var, text_color="red")
        error_label.grid(row=5, column=0, sticky="n")

    def on_login_click(self):
        # Відключаємо кнопку, щоб уникнути подвійних кліків
        self.login_btn.configure(state="disabled", text="Завантаження...")

        email = self.email_var.get().strip()
        password = self.password_var.get().strip()

        if not email or not password:
            self.show_error("Будь ласка, заповніть всі поля")
            self.reset_button()
            return

        # Викликаємо Controller!
        self.login_callback(email, password)

    def show_error(self, message):
        self.error_var.set(message)
        self.email_entry.configure(border_color="red")
        self.password_entry.configure(border_color="red")

    def clear_error(self, *args):
        self.error_var.set("")
        # Повертаємо стандартний колір рамок (можеш використати тему)
        self.email_entry.configure(border_color=["#979DA2", "#565B5E"])
        self.password_entry.configure(border_color=["#979DA2", "#565B5E"])

    def reset_button(self):
        self.login_btn.configure(state="normal", text="Увійти")