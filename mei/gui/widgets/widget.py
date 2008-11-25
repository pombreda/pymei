class Widget(object):
    pass

def get_widget(name, parent=Widget):
    classes = parent.__subclasses__()
    while classes:
        c = classes.pop(0)
        if c.__name__() == name:
            return c

        classes.extend(c.__subclasses__())

    return None
