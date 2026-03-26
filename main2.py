from datetime import datetime
import functools
import os

"""Универсальный декоратор (для использования с параметром или без)"""
def logger(arg=None):
    # Если первый аргумент является функцией, то декоратор был вызван без параметров
    if callable(arg):
        func = arg
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            log_string = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} была вызвана функция {func.__name__} с аргументами {args=}, {kwargs=};"
            result = func(*args, **kwargs)
            log_string += f' результат вызова функции {result=}.'
            with open('main.log', 'a', encoding='utf-8') as file:
                file.write(log_string + '\n')
            return result
        return wrapper
    else:
        # Если первый аргумент НЕ функция, значит, декоратор был вызван с параметрами.
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                path = arg
                log_string = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} была вызвана функция {func.__name__} с аргументами {args=}, {kwargs=};"
                result = func(*args, **kwargs)
                log_string += f' результат вызова функции {result=}.'
                with open(path, 'a', encoding='utf-8') as file:
                    file.write(log_string + '\n')

                return result
            return wrapper
        return decorator


"""Тестирование декоратора logger без параметров"""
def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'

"""Тестирование декоратора logger1 с параметром """
def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'




if __name__ == '__main__':
    test_1()
    test_2()