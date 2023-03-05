from typing import List, Optional


# Класс-конструктор бота
class ModuleBuilder:
    '''Конструктор бота.'''
    # Словарь методов по определенному value_type
    validators = {
        None: None,
    }

    def __init__(
            self, 
            inline: bool, 
            title: str,
            message: str, 
            link: List[Optional[int]] = [], 
            value_type=None, 
            prev: Optional[int] = None,
            *args,
        ) -> None:
        '''ModuleBuidler единожды принимает значения, чтобы по ним в дальнейшем конструировать бота.'''
        self.id = 0
        self.inline = inline
        self.title = title
        self.message = message
        self.link = link
        self.value_type = value_type
        self.prev = prev
        # Где будут создаваться файлы
        self.__workplace = './'
        self.__callback_datas = dict()

    def run(self) -> int:
        '''Основной метод по вызову других методов построения бота.'''
        if 'success':
            return 1
        return 0
    
    # *args поступят при вызове в run
    def __create_message_handler(self, *args) -> None:
        '''Процедура создания хэндлера с заданными параметрами.'''
        if self.inline:
            key = 'data' + str(len(self.__callback_datas.items))
            value = self.__add_inline()
            self.__callback_datas.update({key: value})

    def __add_inline(self) -> str:
        '''Процедура добавления inline к сообщению в модуле. Возвращает data для колбэка'''

    def __add_state_validator(self) -> None:
        '''Процедура добавления проверки состояния в хэндлер.'''

    def __add_state_checkout(self) -> None:
        '''Процедура добавления переключения состояния.'''

    # Думаю для подобных методов(подготовка бд перед созданием модулей) нужен отдельный класс
    def _insert_into_db(self, token):
        '''Запись бота в таблицу ботов.'''

    def __create_callback_handler(self, *args) -> None:
        '''Процедура создания колбэк хэндлера(обработка кнопок)'''

    