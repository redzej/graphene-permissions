import graphene
from graphene import ObjectType, Schema, relay
from graphene_django import DjangoObjectType

from graphene_permissions.mixins import AuthFilter, AuthNode
from graphene_permissions.permissions import AllowStaff, AllowAny
from tests.test_app.models import Owner, Pet


class RestrictedOwnerNode(AuthNode, DjangoObjectType):
    permission_classes = (AllowStaff,)

    class Meta:
        model = Owner
        filter_fields = ('first_name',)
        interfaces = (relay.Node,)


class RestrictedPetNode(AuthNode, DjangoObjectType):
    permission_classes = (AllowStaff,)

    class Meta:
        model = Pet
        filter_fields = ('name',)
        interfaces = (relay.Node,)


class NormalPetNode(AuthNode, DjangoObjectType):
    permission_classes = (AllowAny,)

    class Meta:
        model = Pet
        filter_fields = ('name',)
        interfaces = (relay.Node,)


class NormalOwnerNode(AuthNode, DjangoObjectType):
    permission_classes = (AllowAny,)

    class Meta:
        model = Pet
        filter_fields = ('name',)
        interfaces = (relay.Node,)


class PetsQuery:
    pet = graphene.Field(RestrictedPetNode)
    owner = graphene.Field(RestrictedOwnerNode)

    all_pets = AuthFilter(RestrictedPetNode)
    all_n_pets = AuthFilter(PetNode)
    all_owners = AuthFilter(RestrictedOwnerNode)


class Query(PetsQuery, ObjectType):
    pass


schema = Schema(query=Query)
