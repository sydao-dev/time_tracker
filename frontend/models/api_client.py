import requests

class TimeTrackerAPI:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.token = None
        self.headers = {}
        self.current_user = None

    def login(self, username, password):
        """Робить запит на авторизацію. Повертає (success: bool, message: str)"""
        try:
            response = requests.post(
                f"{self.base_url}/login",
                data={"username": username, "password": password}
            )
            if response.status_code == 200:
                self.token = response.json()["access_token"]
                self.headers = {"Authorization": f"Bearer {self.token}"}
                return True, "Успішно"
            elif response.status_code == 401:
                return False, "Невірний email або пароль"
            else:
                return False, f"Помилка сервера: {response.status_code}"
        except requests.exceptions.ConnectionError:
            return False, "Бекенд недоступний. Перевір сервер."
        except Exception as e:
            return False, str(e)