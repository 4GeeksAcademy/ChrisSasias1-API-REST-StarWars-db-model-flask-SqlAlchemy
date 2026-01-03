import os
from flask_admin import Admin
from models import db, User, Login, Planet, Character, Starship, Favorite
from flask_admin.contrib.sqla import ModelView


class UserModelView(ModelView):
    column_auto_select_related = True
    column_list = ("id", "name", "email", "password", "is_active", "favorites", "logins")


class LoginModelView(ModelView):
    column_auto_select_related = True
    column_list = ("id", "user_id", "user")


class PlanetModelView(ModelView):
    column_auto_select_related = True
    column_list = ("id", "name", "climate", "terrain",
                   "description", "characters", "favorites")


class CharacterModelView(ModelView):
    column_auto_select_related = True
    column_list = ("id", "name", "description",
                   "planet_id", "planet", "favorites")


class StarshipModelView(ModelView):
    column_auto_select_related = True
    column_list = ("id", "name", "model", "manufacturer",
                   "description", "favorites")


class FavoriteModelView(ModelView):
    column_auto_select_related = True
    column_list = (
        "id",
        "user_id", "user",
        "character_id", "character",
        "planet_id", "planet",
        "starship_id", "starship",
    )


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(LoginModelView(Login, db.session))
    admin.add_view(PlanetModelView(Planet, db.session))
    admin.add_view(CharacterModelView(Character, db.session))
    admin.add_view(StarshipModelView(Starship, db.session))
    admin.add_view(FavoriteModelView(Favorite, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))
