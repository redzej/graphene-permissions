import graphene
from graphene import ObjectType, Schema, relay
from graphene_django import DjangoObjectType

from graphene_permissions.mixins import AuthFilter, AuthNode
from graphene_permissions.permissions import AllowAny, AllowStaff
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
        exclude_fields = ('id', 'owner')
        interfaces = (relay.Node,)


class NormalOwnerNode(AuthNode, DjangoObjectType):
    permission_classes = (AllowAny,)

    class Meta:
        model = Pet
        exclude_fields = ('id', 'pet_set')
        filter_fields = ('name',)
        interfaces = (relay.Node,)


class StaffRequiredFilter(AuthFilter):
    permission_classes = (AllowStaff,)


class PetsQuery:
    restricted_pet = graphene.Field(RestrictedPetNode)
    restricted_owner = graphene.Field(RestrictedOwnerNode)
    all_restricted_pets = StaffRequiredFilter(RestrictedPetNode)
    all_restricted_owners = StaffRequiredFilter(RestrictedOwnerNode)

    pet = graphene.Field(NormalPetNode)
    owner = graphene.Field(NormalOwnerNode)
    all_pets = AuthFilter(NormalPetNode)
    all_owners = AuthFilter(NormalOwnerNode)


class Query(PetsQuery, ObjectType):
    pass


schema = Schema(query=Query)
