import graphene
from graphene import Schema, relay
from graphene_django import DjangoObjectType

from tests.models import Owner, Pet


class OwnerNode(DjangoObjectType):
    class Meta:
        model = Owner
        interfaces = (relay.Node,)


class PetNode(DjangoObjectType):
    class Meta:
        model = Pet
        interfaces = (relay.Node,)


class PetsQuery:
    pet = graphene.Field(PetNode)
    owner = graphene.Field(OwnerNode)


schema = Schema(query=PetsQuery)
