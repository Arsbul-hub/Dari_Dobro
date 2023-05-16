from wtforms import ValidationError
FORMATES = {
    "image": ["png", "jpg", "jpeg", "webp"],
    "document": ["pdf", "doc", "docx"]
}

def data_required(form, field):
    if not field.data:
        raise ValidationError("This field is require.")


def image_validation(form, field):

    if field.data and field.data.filename.split(".")[-1] not in FORMATES["image"]:
        raise ValidationError(f"Файл не соответствует форматам: {', '.join(FORMATES['image'])}")


def pdf_validation(form, field):
    if field.data and field.data.filename.split(".")[-1] not in ["pdf"]:
        raise ValidationError(f"Файл не соответствует форматам: {', '.join(FORMATES['document'])}")
