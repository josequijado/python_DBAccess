import hashlib

class Encryption():
    def __init__(self):
        pass

    def encrypt(password):
        # Utilizamos el algoritmo SHA-256 para hashear la contraseña
        hash_object = hashlib.sha256(password.encode())
        hashed_password = hash_object.hexdigest()
        return hashed_password

    def verify(password, hashed_password):
        # Hasheamos la contraseña ingresada y comparamos con la contraseña hasheada almacenada
        return Encryption.encrypt(password) == hashed_password
