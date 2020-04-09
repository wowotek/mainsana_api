# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

from .engine import db


class Budget(db.Model):
    __tablename__ = 'budget'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    trip_id = db.Column(db.ForeignKey('trip.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text)
    budget = db.Column(db.Numeric(22, 2), nullable=False)
    budget_type_id = db.Column(db.ForeignKey('budget_type.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    budget_type = db.relationship('BudgetType', primaryjoin='Budget.budget_type_id == BudgetType.id', backref='budgets')
    trip = db.relationship('Trip', primaryjoin='Budget.trip_id == Trip.id', backref='budgets')



class BudgetType(db.Model):
    __tablename__ = 'budget_type'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), nullable=False)



class Tour(db.Model):
    __tablename__ = 'tour'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    name = db.Column(db.String(45), nullable=False)
    description = db.Column(db.Text)

    user = db.relationship('User', primaryjoin='Tour.user_id == User.id', backref='tours')



class Trip(db.Model):
    __tablename__ = 'trip'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    tour_id = db.Column(db.ForeignKey('tour.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)

    tour = db.relationship('Tour', primaryjoin='Trip.tour_id == Tour.id', backref='trips')



class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    phone = db.Column(db.String(32), nullable=False, unique=True)
