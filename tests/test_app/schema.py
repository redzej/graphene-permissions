import graphene
from graphene import ObjectType, Schema, relay
from graphene_django import DjangoObjectType

from graphene_permissions.mixins import AuthFilter, AuthNode
from graphene_permissions.permissions import AllowAny, AllowStaff, AllowAuthenticated
from tests.test_app.models import Pet


class RestrictedPetNode(AuthNode, DjangoObjectType):
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


class PetsQuery:
    staff_pet = graphene.Field(RestrictedPetNode)
    all_staff_pets = StaffRequiredFilter(RestrictedPetNode)

    user_pet = graphene.Field(AllowAuthenticatedPetNode)
    all_user_pets = AuthFilter(AllowAuthenticatedPetNode)

    pet = graphene.Field(AllowAnyPetNode)
    all_pets = AuthFilter(AllowAnyPetNode)


class Query(PetsQuery, ObjectType):
    pass


schema = Schema(query=Query)
