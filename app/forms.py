from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import BooleanField, EmailField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Optional

from .models import PublicationStatus, Visibility


class RegisterForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired(), Length(min=3, max=80)])
    email = EmailField("Email", validators=[DataRequired(), Length(max=255)])
    full_name = StringField("Имя", validators=[Optional(), Length(max=255)])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField("Повторите пароль", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Зарегистрироваться")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Length(max=255)])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")


class ProfileForm(FlaskForm):
    full_name = StringField("Имя", validators=[Optional(), Length(max=255)])
    bio = TextAreaField("О себе", validators=[Optional(), Length(max=2000)])
    submit = SubmitField("Сохранить")


class ItemForm(FlaskForm):
    title = StringField("Название предмета", validators=[DataRequired(), Length(max=255)])
    period = StringField("Период создания", validators=[Optional(), Length(max=120)])
    material = StringField("Материал", validators=[Optional(), Length(max=120)])
    comments = TextAreaField("Комментарии", validators=[Optional(), Length(max=5000)])

    manufacturer_id = SelectField("Производитель", coerce=int, validators=[Optional()])
    sculptor_id = SelectField("Скульптор", coerce=int, validators=[Optional()])
    artist_id = SelectField("Художник", coerce=int, validators=[Optional()])
    shape_id = SelectField("Форма", coerce=int, validators=[Optional()])
    painting_style_id = SelectField("Роспись", coerce=int, validators=[Optional()])

    publication_status = SelectField(
        "Статус публикации",
        choices=[(PublicationStatus.DRAFT, "Черновик"), (PublicationStatus.PUBLISHED, "Опубликовано")],
        validators=[DataRequired()],
    )
    visibility = SelectField(
        "Видимость",
        choices=[(Visibility.PUBLIC, "Публичный"), (Visibility.PRIVATE, "Только владелец")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Сохранить")


class UploadPhotoForm(FlaskForm):
    photos = FileField(
        "Фотографии",
        validators=[
            FileRequired(),
            FileAllowed(["jpg", "jpeg", "png", "webp"], "Только изображения JPG/PNG/WEBP."),
        ],
        render_kw={"multiple": True, "accept": ".jpg,.jpeg,.png,.webp"},
    )
    submit = SubmitField("Загрузить")


class LookupForm(FlaskForm):
    name = StringField("Название", validators=[DataRequired(), Length(max=120)])
    submit = SubmitField("Сохранить")
