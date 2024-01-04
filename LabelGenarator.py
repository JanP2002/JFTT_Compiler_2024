def _generate_label(label_type, number):
    return label_type + str(number) + ":"


class LabelGenerator:
    _instance = None
    if_end_label_counter = 0
    else_label_counter = 0
    IF_END = "IF_END"
    ELSE = "ELSE"

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        pass

    def next_if_end_label(self):
        self.if_end_label_counter += 1
        return _generate_label(self.IF_END, self.if_end_label_counter)

    def next_else_label(self):
        self.else_label_counter += 1
        return _generate_label(self.ELSE, self.else_label_counter)
