import platform
from typing import Optional, TypedDict, cast
from .Credentials import Credentials
import keyring

class WindowsCredentialsDict(TypedDict):
    UserName: str
    CredentialBlob: bytes

class CredentialManager:
    def __init__(self):
        self.os_type: str = platform.system()

    def get_credentials(self, cred_name: str) -> Credentials:
        if self.os_type == 'Windows':
            return self._get_windows_credentials(cred_name)
        elif self.os_type == 'Darwin':
            return self._get_mac_credentials(cred_name)
        else:
            raise NotImplementedError(f'OS {self.os_type} not supported.')

    def _get_windows_credentials(self, cred_name: str) -> Credentials:
        import win32cred
        cred: Optional[WindowsCredentialsDict] = cast(
            Optional[WindowsCredentialsDict], 
            win32cred.CredRead(Type=win32cred.CRED_TYPE_GENERIC, TargetName=cred_name)
        )
        if cred is None:
            raise Exception("Credentials not found")
        return Credentials(Username=cred['UserName'], Password=cred['CredentialBlob'].decode('utf-16-le'))


    def _get_mac_credentials(self, cred_name: str) -> Credentials:
        username = keyring.get_password(cred_name, 'username')
        if username is None:
            raise Exception("cred username not found")
        password = keyring.get_password(cred_name, 'password')
        if password is None:
            raise Exception("cred password not found")
        return Credentials(Username=username, Password=password)
