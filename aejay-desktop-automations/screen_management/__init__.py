import platform

from .FunkyState import FunkyState

os_type: str = platform.system()

if os_type == 'Windows':
    from .WindowsFunkifier import WindowsFunkifier as Funkifier
elif os_type == 'Darwin':
    from .MacFunkifier import MacFunkifier as Funkifier
else:
    raise NotImplementedError(f'OS {os_type} not supported.')

__all__ = ['FunkyState','Funkifier']
