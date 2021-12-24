from __future__ import annotations


from functools import wraps


def same_type_operation(oper_str: str):
    def decorator(func):
        return _same_type_operation(func, oper_str)

    return decorator


def _same_type_operation(func, oper_str: str):
    @wraps(func)
    def wrapper(self, other):
        if not isinstance(other, type(self)):
            raise TypeError(
                f"{oper_str} not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'"
            )
        return func(self, other)

    return wrapper
