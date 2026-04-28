class CustomExceptionA(Exception):
    """
    Пользовательское исключение A
    Возникает при невыполнении определенного условия
    Возвращает статус 400 (Bad Request)
    """
    def __init__(self, detail: str = "Custom Exception A occurred"):
        self.detail = detail
        self.status_code = 400

class CustomExceptionB(Exception):
    """
    Пользовательское исключение B
    Возникает когда ресурс не найден
    Возвращает статус 404 (Not Found)
    """
    def __init__(self, detail: str = "Resource not found"):
        self.detail = detail
        self.status_code = 404