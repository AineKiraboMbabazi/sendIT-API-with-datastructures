users = []


class User:
    def __init__(self, email, password):
        self.userId = len(users)+1
        self.email = email
        self.password = password

    def to_dictionary(self):
        user = {
            "userId": self.userId,
            "email": self.email,
            "password": self.password
        }
        return user
