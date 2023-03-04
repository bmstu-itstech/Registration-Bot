from typing import List, Optional

from .modulebuilder import ModuleBuilder


class Module(ModuleBuilder):
    def __init__(self, *args) -> None:
        # Такая конструкция вроде должна работать, никогда не работал с наследованием
        ModuleBuilder.__init__(self, *args)

    def create_module(self) -> None:
        '''Создание сущности модуля в БД.'''
        # Метод записи в БД, который возвращает текущий id модуля в БД
        self.id = mock()
    
    def connect_modules(self) -> None:
        '''Связывание 2-х модулей.'''
        pass

    def read_module(self, title: Optional[str] = None, id: Optional[int] = None) -> None | any:
        '''Проверка модуля в БД по id или title.'''
        if not(title or id):
            return


# Универсальная функция(глушилка)
def mock(*args, **kwargs) -> any:
    pass