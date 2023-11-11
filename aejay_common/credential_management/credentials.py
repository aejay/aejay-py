"""
A module for managing credentials.
"""
import keyring


def get_credentials(cred_name: str) -> tuple[str, str]:
    """
    Attempts to get the credentials for the given cred_name from the keyring.
    """
    username = keyring.get_password(cred_name, "username")
    if username is None:
        raise KeyError(f"cred {cred_name} username not found")
    password = keyring.get_password(cred_name, "password")
    if password is None:
        raise KeyError(f"cred {cred_name} password not found")
    return username, password
