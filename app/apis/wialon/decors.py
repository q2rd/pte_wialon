from functools import wraps


def session(func):
    """
    Выполняет логин для API Wialon`a записывая текщую сессию в объект.
    После завершения функции сессия автоматически закрывается.

    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        res = self.token_login(token=self.token)
        self.sid = res["eid"]
        # print("лог ин")
        try:
            # print("выполнение функции")
            return func(self, *args, **kwargs)
        finally:
            # print("лог аут")
            self.core_logout()
            self.sid = None

    return wrapper
