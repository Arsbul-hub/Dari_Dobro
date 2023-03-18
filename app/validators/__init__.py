from wtforms import ValidationError


def image_validation(form, field):
    if field.data and field.data.filename.split(".")[-1] not in ["png", "jpg", "jpeg", "webp"]:
        raise ValidationError("Файл не соответствует формату!")


def pdf_validation(form, field):
    if field.data and field.data.filename.split(".")[-1] not in ["pdf"]:
        raise ValidationError("Файл не соответствует формату!")
