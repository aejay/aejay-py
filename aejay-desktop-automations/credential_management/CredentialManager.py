from typing import Optional
import platform
from .Credentials import Credentials

class CredentialManager:
    def __init__(self):
        self.os_type: str = platform.system()

    def get_credentials(self, cred_name: str) -> Optional[Credentials]:
        if self.os_type == 'Windows':
            return self._get_windows_credentials(cred_name)
        elif self.os_type == 'Darwin':
            return self._get_mac_credentials(cred_name)
        else:
            raise NotImplementedError(f'OS {self.os_type} not supported.')

    def _get_windows_credentials(self, cred_name: str) -> Optional[Credentials]:
        import win32cred
        try:
            cred = win32cred.CredRead(Type=win32cred.CRED_TYPE_GENERIC, TargetName=cred_name)
            return Credentials(Username=cred['UserName'], Password=cred['CredentialBlob'].decode('utf-16-le'))
        except Exception as e:
            print(f'Error: {str(e)}')
            return None

    def _get_mac_credentials(self, cred_name: str) -> Optional[Credentials]:
        import keyring
        try:
            password = keyring.get_password(cred_name, 'username')
            return Credentials(Username='username', Password=password)
        except Exception as e:
            print(f'Error: {str(e)}')
            return None
