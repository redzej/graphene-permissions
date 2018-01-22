import graphene
from graphene import Schema, relay
from graphene_django import DjangoObjectType
from graphene_permissions.permissions import AllowStaff, AllowAny
from graphene_permissions.mixins import AuthFilter, AuthNode, AuthMutation
from tests.test_app.models import Owner, Pet


class OwnerNode(AuthNode, DjangoObjectType):
    permission_classes = (AllowStaff,)

    class Meta:
        model = Owner
        interfaces = (relay.Node,)


class PetNode(AuthNode, DjangoObjectType):
    permission_classes = (AllowStaff,)

    class Meta:
        model = Pet
        interfaces = (relay.Node,)


class PetsQuery:
    pet = graphene.Field(PetNode)
    owner = graphene.Field(OwnerNode)

    all_pets = AuthFilter(PetNode)
    all_owners = AuthFilter(OwnerNode)


schema = Schema(query=PetsQuery)
