import secrets


class SecretsManager:

    def generate_secret(self):

        return secrets.token_hex(32)