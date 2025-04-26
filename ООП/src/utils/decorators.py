from functools import wraps
from .exceptions import PermissionDeniedError

def check_permissions(required_permission: str):
    """Декоратор для проверки прав доступа пользователя.

    Args:
        required_permission: Требуемое разрешение для выполнения действия.
    Raises:
        PermissionDeniedError: Если у пользователя нет необходимого разрешения.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Предполагается, что объект имеет атрибут customer с permissions
            if not hasattr(self, 'customer') or required_permission not in self.customer.permissions:
                raise PermissionDeniedError(
                    f"У пользователя нет разрешения '{required_permission}' для выполнения действия '{func.__name__}'"
                )
            return func(self, *args, **kwargs)
        return wrapper
    return decorator