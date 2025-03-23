class CustomValidators:

    @staticmethod
    def text_minimal(value):
        if len(value) <= 3:
            raise ValueError("Title 3 tadan kam bo'lishi mumkin emas!")
        return value

    @staticmethod
    def text_maximal(value):
        pass
