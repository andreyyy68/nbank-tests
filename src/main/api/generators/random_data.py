import random
from faker import Faker

fake = Faker()

class RandomData:
    @staticmethod
    def generate_username():
        return ''.join(fake.random_letters(random.randint(1, 2)))