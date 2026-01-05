from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    logins: Mapped[list['Login']] = relationship(back_populates='user')
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)
    favorites: Mapped[list['Favorite']] = relationship(back_populates='user')

    def __repr__(self):
        return f'Usuario {self.email}'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'is_active': self.is_active,
        }


class Login(db.Model):
    __tablename__ = 'logins'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped['User'] = relationship(back_populates='logins')

    def __repr__(self):
        return f'<Login id={self.id} user_id={self.user_id}>'

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id
        }


class Planet(db.Model):
    __tablename__ = 'planets'

    id: Mapped[int] = mapped_column(primary_key=True)
    climate: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(150), nullable=False)
    terrain: Mapped[str] = mapped_column(String(100), nullable=False)

    characters: Mapped[list['Character']] = relationship(back_populates='planet')
    favorites: Mapped[list['Favorite']] = relationship(back_populates='planet')

    def __repr__(self):
        return f'<Planet id={self.id} name="{self.name}">'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'climate': self.climate,
            'terrain': self.terrain,
            'description': self.description,
        }


class Character(db.Model):
    __tablename__ = 'characters'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25), nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id'), nullable=True)
    planet: Mapped['Planet'] = relationship(back_populates='characters')
    favorites: Mapped[list['Favorite']] = relationship(back_populates='character')

    def __repr__(self):
        return f'personaje {self.name}'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'height': self.height,
            'description': self.description,
            'planet_id': self.planet_id,
        }


class Starship(db.Model):
    __tablename__ = 'starships'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    model: Mapped[str] = mapped_column(String(80), nullable=False)
    manufacturer: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=False)

    favorites: Mapped[list['Favorite']] = relationship(back_populates='starship')

    def __repr__(self):
        return f'<Starship id={self.id} name="{self.name}" model="{self.model}">'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'model': self.model,
            'manufacturer': self.manufacturer,
            'description': self.description,
        }


class Favorite(db.Model):
    __tablename__ = 'favorites'

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    character_id: Mapped[int] = mapped_column(ForeignKey('characters.id'), nullable=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id'), nullable=True)
    starship_id: Mapped[int] = mapped_column(ForeignKey('starships.id'), nullable=True)

    user: Mapped['User'] = relationship(back_populates='favorites')
    character: Mapped['Character'] = relationship(back_populates='favorites')
    planet: Mapped['Planet'] = relationship(back_populates='favorites')
    starship: Mapped['Starship'] = relationship(back_populates='favorites')

    def __repr__(self):
        return f'Favorite(user_id={self.user_id}, character_id={self.character_id}, planet_id={self.planet_id}, starship_id={self.starship_id})'

    def serialize(self):
        fav_type = None
        item = None

        if self.character_id is not None:
            fav_type = 'character'
            item = self.character.serialize() if self.character else {'id': self.character_id, 'name': None}
        elif self.planet_id is not None:
            fav_type = 'planet'
            item = self.planet.serialize() if self.planet else {'id': self.planet_id, 'name': None}
        elif self.starship_id is not None:
            fav_type = 'starship'
            item = self.starship.serialize() if self.starship else {'id': self.starship_id, 'name': None}

        return {
            'id': self.id,
            'type': fav_type,
            'item': item
        }
