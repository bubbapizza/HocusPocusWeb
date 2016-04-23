from wtforms import (
    Form,
    StringField,
    PasswordField,
    validators,
)
from wtforms.validators import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from ..models.user import User


class OpenDoorForm(Form):
    ip_address = StringField(validators=[
        validators.Required(),
    ])
    password = PasswordField(validators=[
        validators.Required(),
    ])

    def __init__(self, dbsession, *args, **kwargs):
        self.dbsession = dbsession
        super().__init__(*args, **kwargs)

    def validate_password(self, field):
        password = field.data
        try:
            user = self.dbsession.query(User)\
                .filter_by(ip_address=self.ip_address.data).one()
        except NoResultFound:
            raise ValidationError("Invalid Credentials.")
        else:
            if not user.check_password(password):
                raise ValidationError("Invalid Credentials.")
