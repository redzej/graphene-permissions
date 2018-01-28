from http import HTTPStatus

import graphene
from django.contrib.auth.models import User
from graphene import ObjectType, Schema, relay
from graphene.relay import ClientIDMutation
from graphene_django import DjangoObjectType
from graphql_relay import from_global_id

from graphene_permissions.mixins import AuthFilter, AuthMutation, AuthNode
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
    staff_pet = relay.Node.Field(StaffRequiredPetNode)
    all_staff_pets = StaffRequiredFilter(StaffRequiredPetNode)

    user_pet = relay.Node.Field(AllowAuthenticatedPetNode)
    all_user_pets = AllowAuthenticatedFilter(AllowAuthenticatedPetNode)

    pet = relay.Node.Field(AllowAnyPetNode)
    all_pets = AuthFilter(AllowAnyPetNode)


class StaffAddPet(AuthMutation, ClientIDMutation):
    permission_classes = (AllowStaff,)

    class Input:
        name = graphene.String()
        race = graphene.String()
        owner = graphene.ID()

    pet = graphene.Field(AllowAnyPetNode)
    status = graphene.Int()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        if cls.has_permission(root, info, input):
            owner = User.objects.get(pk=from_global_id(input['owner'])[1])
            pet = Pet.objects.create(name=input['name'], race=input['race'], owner=owner)
            return AddPet(pet=pet, status=HTTPStatus.CREATED)
        return AddPet(pet=None, status=HTTPStatus.BAD_REQUEST)


class AuthenticatedAddPet(AuthMutation, ClientIDMutation):
    permission_classes = (AllowAuthenticated,)

    class Input:
        name = graphene.String()
        race = graphene.String()
        owner = graphene.ID()

    pet = graphene.Field(AllowAnyPetNode)
    status = graphene.Int()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        if cls.has_permission(root, info, input):
            owner = User.objects.get(pk=from_global_id(input['owner'])[1])
            pet = Pet.objects.create(name=input['name'], race=input['race'], owner=owner)
            return AuthenticatedAddPet(pet=pet, status=HTTPStatus.CREATED)
        return AuthenticatedAddPet(pet=None, status=HTTPStatus.BAD_REQUEST)


class AddPet(AuthMutation, ClientIDMutation):
    permission_classes = (AllowAny,)

    class Input:
        name = graphene.String()
        race = graphene.String()
        owner = graphene.ID()

    pet = graphene.Field(AllowAnyPetNode)
    status = graphene.Int()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        if cls.has_permission(root, info, input):
            owner = User.objects.get(pk=from_global_id(input['owner'])[1])
            pet = Pet.objects.create(name=input['name'], race=input['race'], owner=owner)
            return AddPet(pet=pet, status=HTTPStatus.CREATED)
        return AddPet(pet=None, status=HTTPStatus.BAD_REQUEST)


class PetsMutation:
    staff_add_pet = StaffAddPet.Field()
    authenticated_add_pet = AuthenticatedAddPet.Field()
    add_pet = AddPet.Field()


class Query(PetsQuery, ObjectType):
    pass


class Mutation(PetsMutation, ObjectType):
    pass


schema = Schema(query=Query, mutation=Mutation)
