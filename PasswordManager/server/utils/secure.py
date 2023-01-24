from cryptography.fernet import Fernet


key = b"OJpSqD8ZzNAh2qcTGO-YhumySXqLHHXs514iV5kKJD4="

def encrypt(data: str) -> str:
    return Fernet(key).encrypt(data.encode()).decode()
