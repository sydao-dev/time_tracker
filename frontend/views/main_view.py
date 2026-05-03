import customtkinter as ctk


class MainView(ctk.CTkFrame):
    def __init__(self, parent, nav_callback):
        super().__init__(parent, corner_radius=0)
        self.nav_callback = nav_callback
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._build_sidebar()
        self._build_content_area()

    def _build_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="TimeTracker", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))

        self.btn_timer = ctk.CTkButton(self.sidebar_frame, text="⏱ Таймер", anchor="w",
                                       command=lambda: self.nav_callback("timer"))
        self.btn_timer.grid(row=1, column=0, padx=20, pady=10)

        self.btn_projects = ctk.CTkButton(self.sidebar_frame, text="📁 Проєкти", anchor="w",
                                          command=lambda: self.nav_callback("projects"))
        self.btn_projects.grid(row=2, column=0, padx=20, pady=10)

        self.btn_reports = ctk.CTkButton(self.sidebar_frame, text="📊 Аналітика", anchor="w",
                                         command=lambda: self.nav_callback("reports"))
        self.btn_reports.grid(row=3, column=0, padx=20, pady=10)

        self.btn_logout = ctk.CTkButton(self.sidebar_frame, text="🚪 Вихід", anchor="w", fg_color="transparent",
                                        border_width=1, text_color=("gray10", "#DCE4EE"),
                                        command=lambda: self.nav_callback("logout"))
        self.btn_logout.grid(row=6, column=0, padx=20, pady=20)

    def _build_content_area(self):
        # Контейнер для екранів (Таймер, Проєкти тощо)
        self.content_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Щоб внутрішні фрейми розтягувалися на весь контейнер
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

    def get_content_container(self):
        """Повертає контейнер, куди контролер буде вставляти інші View"""
        return self.content_frame