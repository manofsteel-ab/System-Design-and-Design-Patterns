
"""
A sample example(Localizer) of using factory design pattern
"""

class FrenchLocalizer:

    def __init__(self):
        self.translations = {
            "car": "voiture", "bike": "bicyclette", "cycle":"cyclette"
        }

    def localize(self, message):
        return self.translations.get(message, message)

class EnglishLocalizer:
    def localize(self, msg):
        return msg

def factory(language='English'):
    localizers = {
        'English': EnglishLocalizer,
        'French': FrenchLocalizer
    }
    return localizers[language]()

if __name__ == '__main__':
    f = factory(language='French')
    e = factory(language='English')

    message = ["car", "bike", "cycle"]

    for msg in message:
        print(f.localize(msg))
        print(e.localize(msg))
