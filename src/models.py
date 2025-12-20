from typing import Optional
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    logins: Mapped[list['Login']] = relationship(back_populates='user')
    favorites: Mapped[list['Favorite']] = relationship(back_populates='user')


class Login(db.Model):
    __tablename__ = 'logins'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped['User'] = relationship(back_populates='logins')


class Planet(db.Model):
    __tablename__ = 'planets'

    id: Mapped[int] = mapped_column(primary_key=True)
    climate: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(150), nullable=False)
    terrain: Mapped[str] = mapped_column(String(100), nullable=False)
    characters: Mapped[list['Character']] = relationship(back_populates='planet')
    favorites: Mapped[list['Favorite']] = relationship(back_populates='planet')


class Character(db.Model):
    __tablename__ = 'characters'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id'), nullable=True)
    planet: Mapped['Planet'] = relationship(back_populates='characters')
    favorites: Mapped[list['Favorite']] = relationship(back_populates='character')


class Starship(db.Model):
    __tablename__ = 'starships'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    model: Mapped[str] = mapped_column(String(80), nullable=False)
    manufacturer: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    favorites: Mapped[list['Favorite']] = relationship(back_populates='starship')


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
