_LOCALE: dict = {}

def load_labels(labels: dict):
    global _LOCALE #pylint: disable = global-statement
    _LOCALE = labels

def translate(label, scope = None):
    try:
        levels = label.split('.')
        if scope is not None:
            levels = scope.split('.') + levels
        value =  _LOCALE
        for level in levels:
            value = value[level]
        return value
    except KeyError as err:
        raise RuntimeError('Missing label from locale') from err

t = translate
