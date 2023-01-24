from cryptography.fernet import Fernet


key = b"OJpSqD8ZzNAh2qcTGO-YhumySXqLHHXs514iV5kKJD4="

def decrypt(data: str) -> str:
    return Fernet(key).decrypt(data.encode()).decode()
