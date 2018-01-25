import graphene
from graphene import ObjectType, Schema, relay
from graphene_django import DjangoObjectType

from graphene_permissions.mixins import AuthFilter, AuthNode
from graphene_permissions.permissions import AllowAny, AllowStaff
from tests.test_app.models import User, Pet


class RestrictedUserNode(AuthNode, DjangoObjectType):
    permission_classes = (AllowStaff,)

    class Meta:
        model = User
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
        exclude_fields = ('id', 'User')
        interfaces = (relay.Node,)


class NormalUserNode(AuthNode, DjangoObjectType):
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
    restricted_user = graphene.Field(RestrictedUserNode)
    all_restricted_pets = StaffRequiredFilter(RestrictedPetNode)
    all_restricted_users = StaffRequiredFilter(RestrictedUserNode)

    pet = graphene.Field(NormalPetNode)
    user = graphene.Field(NormalUserNode)
    all_pets = AuthFilter(NormalPetNode)
    all_users = AuthFilter(NormalUserNode)


class Query(PetsQuery, ObjectType):
    pass


schema = Schema(query=Query)
