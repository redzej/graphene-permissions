import graphene
from graphene import ObjectType, Schema, relay
from graphene_django import DjangoObjectType

from graphene_permissions.mixins import AuthFilter, AuthNode
from graphene_permissions.permissions import AllowAny, AllowStaff
from tests.test_app.models import Pet, User


class UserNode(AuthNode, DjangoObjectType):
    permission_classes = (AllowStaff,)

    class Meta:
        model = User
        filter_fields = ('username',)
        interfaces = (relay.Node,)


class PetNode(AuthNode, DjangoObjectType):
    permission_classes = (AllowStaff,)

    class Meta:
        model = Pet
        filter_fields = ('name',)
        interfaces = (relay.Node,)


class OwnedPetNode(AuthNode, DjangoObjectType):
    permission_classes = (AllowAny,)

    class Meta:
        model = Pet
        filter_fields = ('name',)
        interfaces = (relay.Node,)


class InfoPetNode(AuthNode, DjangoObjectType):
    permission_classes = (AllowAny,)

    class Meta:
        model = Pet
        exclude_fields = ('owner',)
        filter_fields = ('name',)
        interfaces = (relay.Node,)


class StaffRequiredFilter(AuthFilter):
    permission_classes = (AllowStaff,)


class PetsQuery:
    pet = graphene.Field(PetNode)
    user = graphene.Field(UserNode)
    all_pets = StaffRequiredFilter(PetNode)
    all_owners = StaffRequiredFilter(UserNode)

    my_pet = graphene.Field(OwnedPetNode)
    my_all_pets = AuthFilter(PetNode)

    other_pet = graphene.Field(InfoPetNode)
    other_all_pets = AuthFilter(InfoPetNode)


class Query(PetsQuery, ObjectType):
    pass


schema = Schema(query=Query)
