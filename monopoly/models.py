from django.db import models
from pprint import pprint
import json

class Game(models.Model):
    id = models.AutoField(primary_key=True)
    private = models.BooleanField(default=False)
    in_progress = models.BooleanField(default=False)

    def __str__(self):
        return "ID: {0}\nPrivate: {1}\nIn progress: {2}".format(
                self.id, self.private, self.in_progress)

class Square(models.Model):
    id = models.AutoField(primary_key=True)
    position = models.IntegerField(default=0)
    game = models.ForeignKey(Game)
    title = models.CharField(default="Square", max_length=255)

    def __str__(self):
        return "Game ID: {0}\nPosition: {1}\nTitle: {2}".format(
                self.game.id, self.position, self.title)

class Player(models.Model):
    session_id = models.CharField(primary_key=True, max_length=32)
    joined = models.IntegerField(default=0)
    game = models.ForeignKey(Game)
    name = models.CharField(default="Player", max_length=255)
    money = models.IntegerField(default=1500)
    square = models.ForeignKey(Square)
    plays_in_turns = models.IntegerField(default=0)
    in_jail_for = models.IntegerField(default=0)
    rolled_this_turn = models.BooleanField(default=False)
    drew_card_this_turn = models.BooleanField(default=False)

    def is_in_jail(self):
        assert self.in_jail_for >=0 and self.in_jail_for <= 3, "Unexpected number of jail turns: {0}.".format(self.in_jail_for)
        return self.in_jail_for > 0

    def __str__(self):
        return "Session ID: {0}\nGame ID: {1}\nName: {2}\nMoney: {3}\nSquare: {4}\nPlays in turns: {5}".format(
            self.session_id, self.game.id, self.name, self.money, self.square.position, self.plays_in_turns)

class Street(models.Model):
    id = models.AutoField(primary_key=True)
    color = models.CharField(max_length=16)
    game = models.ForeignKey(Game)

    def __str__(self):
        return "Game ID: {0}\nColor: {1}".format(
            self.game.id, self.color)

class Property(models.Model):
    square = models.OneToOneField(Square)
    street = models.ForeignKey(Street)
    owned_by = models.ForeignKey(Player, null=True)
    price = models.IntegerField(default=0)
    tax_site = models.IntegerField(default=0)
    tax_1house = models.IntegerField(default=0)
    tax_2house = models.IntegerField(default=0)
    tax_3house = models.IntegerField(default=0)
    tax_4house = models.IntegerField(default=0)
    tax_hotel = models.IntegerField(default=0)
    mortgage_price = models.IntegerField(default=0)
    is_mortgaged = models.BooleanField(default=False)

    def __str__(self):
        return "Square: {0}\nOwned by: {1}\nStreet: {2}\nIs mortgaged: {3}".format(
            self.square.position, (self.owned_by.session_id if self.owned_by is not None else "Nobody"), self.street.color, self.is_mortgaged)

class Utility(models.Model):
    square = models.OneToOneField(Square)
    owned_by = models.ForeignKey(Player, null=True)
    price = models.IntegerField(default=0)
    mortgage_price = models.IntegerField(default=0)
    is_mortgaged = models.BooleanField(default=False)
    tax_site = models.IntegerField(default=0)

    def __str__(self):
        return "Square: {0}\nOwned by: {1}\nIs mortgaged: {2}".format(
            self.square.position, (self.owned_by.session_id if self.owned_by is not None else "Nobody"), self.is_mortgaged)

class Effect(models.Model):
    type = models.CharField(max_length=128, unique=True)
    param = models.IntegerField(default=0, null=True)

    def __str__(self):
        return "Type: {0}\nParam: {1}".format(
            self.type, self.param)

class Special(models.Model):
    square = models.OneToOneField(Square)
    effect = models.ForeignKey(Effect, null=True)

    def __str__(self):
        return "Square: {0}\nEffect: {1}".format(
            self.square.position, (self.effect.type if self.effect is not None else "None"))

