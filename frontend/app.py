import customtkinter as ctk
from models.api_client import TimeTrackerAPI
from controllers.auth_controller import AuthController
from controllers.main_controller import MainController

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Time Tracker")
        self.geometry("900x600")
        self.minsize(800, 500)

        self.api = TimeTrackerAPI()

        self.auth_controller = AuthController(
            root=self,
            model=self.api,
            on_success_callback=self.show_main_app
        )

        self.main_controller = MainController(
            root=self,
            model=self.api,
            on_logout_callback=self.show_auth
        )

        self.auth_controller.show()

    def show_main_app(self):
        """Запускається після успішного логіну"""
        self.main_controller.show()

    def show_auth(self):
        """Запускається після виходу з системи"""
        self.auth_controller.show()


if __name__ == "__main__":
    app = App()
    app.mainloop()