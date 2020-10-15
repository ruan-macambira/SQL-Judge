_LOCALE: dict = {}

def load_labels(labels: dict):
    global _LOCALE
    _LOCALE = labels

def translate(label):
    try:
        return _LOCALE[label]
    except KeyError as err:
        raise RuntimeError('Missing label from locale') from err

t = translate
