import graphene
from graphene import ObjectType, Schema, relay
from graphene_django import DjangoObjectType

from graphene_permissions.mixins import AuthFilter, AuthNode
from graphene_permissions.permissions import (AllowAny, AllowAuthenticated,
                                              AllowStaff)
from tests.test_app.models import Pet


class StaffRequiredPetNode(AuthNode, DjangoObjectType):
    permission_classes = (AllowStaff,)

    class Meta:
        model = Pet
        filter_fields = ('name',)
        interfaces = (relay.Node,)


class AllowAuthenticatedPetNode(AuthNode, DjangoObjectType):
    permission_classes = (AllowAuthenticated,)

    class Meta:
        model = Pet
        filter_fields = ('name',)
        interfaces = (relay.Node,)


class AllowAnyPetNode(AuthNode, DjangoObjectType):
    permission_classes = (AllowAny,)

    class Meta:
        model = Pet
        filter_fields = ('name',)
        interfaces = (relay.Node,)


class StaffRequiredFilter(AuthFilter):
    permission_classes = (AllowStaff,)


class AllowAuthenticatedFilter(AuthFilter):
    permission_classes = (AllowAuthenticated,)


class PetsQuery:
    staff_pet = graphene.Field(StaffRequiredPetNode)
    all_staff_pets = StaffRequiredFilter(StaffRequiredPetNode)

    user_pet = graphene.Field(AllowAuthenticatedPetNode)
    all_user_pets = AllowAuthenticatedFilter(AllowAuthenticatedPetNode)

    pet = graphene.Field(AllowAnyPetNode)
    all_pets = AuthFilter(AllowAnyPetNode)


class Query(PetsQuery, ObjectType):
    pass


schema = Schema(query=Query)
