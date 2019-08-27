import inspect


def log(*args):
    func_name = inspect.stack()[1].function

    print(func_name, *args)
