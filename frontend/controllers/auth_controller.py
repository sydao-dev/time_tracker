from views.auth_view import AuthView

class AuthController:
    def __init__(self, root, model, on_success_callback):
        self.root = root
        self.model = model
        self.on_success_callback = on_success_callback  # Що робити після успішного логіну (перейти на головний екран)

        # Створюємо View і передаємо їй функцію handle_login
        self.view = AuthView(self.root, self.handle_login)

    def show(self):
        """Відображає вікно авторизації"""
        self.view.pack(fill="both", expand=True)

    def hide(self):
        """Ховає вікно авторизації"""
        self.view.pack_forget()

    def handle_login(self, email, password):
        """Цю функцію викликає View, коли юзер тисне кнопку"""
        success, message = self.model.login(email, password)

        if success:
            print("Логін успішний! Токен:", self.model.token)
            self.hide()  # Ховаємо екран авторизації
            self.on_success_callback()  # Кажемо головному додатку запускати основний інтерфейс
        else:
            self.view.show_error(message)
            self.view.reset_button()