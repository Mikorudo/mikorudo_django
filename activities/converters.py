from datetime import datetime

class DateConverter:
    regex = "(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-20\d{2}"

    def to_python(self, value):
        # Преобразуем строку в объект datetime
        return datetime.strptime(value, "%d-%m-%Y").date()

    def to_url(self, value):
        # Преобразуем объект даты в строку формата DD-MM-YYYY
        return value.strftime("%d-%m-%Y")