import graphene
from graphene import ObjectType, Schema, relay
from graphene_django import DjangoObjectType

from graphene_permissions.mixins import AuthFilter, AuthNode
from graphene_permissions.permissions import AllowStaff
from tests.test_app.models import Owner, Pet


class OwnerNode(AuthNode, DjangoObjectType):
    permission_classes = (AllowStaff,)

    class Meta:
        model = Owner
        filter_fields = ('first_name',)
        interfaces = (relay.Node,)


class PetNode(AuthNode, DjangoObjectType):
    permission_classes = (AllowStaff,)

    class Meta:
        model = Pet
        filter_fields = ('name',)
        interfaces = (relay.Node,)


class PetsQuery:
    pet = graphene.Field(PetNode)
    owner = graphene.Field(OwnerNode)

    all_pets = AuthFilter(PetNode)
    all_owners = AuthFilter(OwnerNode)


class Query(PetsQuery, ObjectType):
    pass


schema = Schema(query=Query)
