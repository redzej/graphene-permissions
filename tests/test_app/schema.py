from http import HTTPStatus

import graphene
from django.contrib.auth.models import User
from graphene import ObjectType, Schema, relay
from graphene.relay import ClientIDMutation
from graphene_django import DjangoObjectType
from graphql_relay import from_global_id

from graphene_permissions.mixins import AuthFilter, AuthMutation, AuthNode
from graphene_permissions.permissions import (
    AllowAny,
    AllowAuthenticated,
    AllowStaff,
    AllowSuperuser,
)
from tests.test_app.models import Pet


class SuperUserRequiredPetNode(AuthNode, DjangoObjectType):
    permission_classes = (AllowSuperuser,)

    class Meta:
        model = Pet
        filter_fields = ('name',)
        interfaces = (relay.Node,)


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


class SuperUserRequiredFilter(AuthFilter):
    permission_classes = (AllowSuperuser,)


class StaffRequiredFilter(AuthFilter):
    permission_classes = (AllowStaff,)


class AllowAuthenticatedFilter(AuthFilter):
    permission_classes = (AllowAuthenticated,)


class PetsQuery:
    superuser_pet = relay.Node.Field(SuperUserRequiredPetNode)
    all_superuser_pets = SuperUserRequiredFilter(SuperUserRequiredPetNode)

    staff_pet = relay.Node.Field(StaffRequiredPetNode)
    all_staff_pets = StaffRequiredFilter(StaffRequiredPetNode)

    user_pet = relay.Node.Field(AllowAuthenticatedPetNode)
    all_user_pets = AllowAuthenticatedFilter(AllowAuthenticatedPetNode)

    pet = relay.Node.Field(AllowAnyPetNode)
    all_pets = AuthFilter(AllowAnyPetNode)


class SuperUserAddPet(AuthMutation, ClientIDMutation):
    permission_classes = (AllowSuperuser,)

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
            return SuperUserAddPet(pet=pet, status=HTTPStatus.CREATED)
        return SuperUserAddPet(pet=None, status=HTTPStatus.BAD_REQUEST)


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
            return StaffAddPet(pet=pet, status=HTTPStatus.CREATED)
        return StaffAddPet(pet=None, status=HTTPStatus.BAD_REQUEST)


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
    superuser_add_pet = SuperUserAddPet.Field()
    staff_add_pet = StaffAddPet.Field()
    authenticated_add_pet = AuthenticatedAddPet.Field()
    add_pet = AddPet.Field()


class Query(PetsQuery, ObjectType):
    pass


class Mutation(PetsMutation, ObjectType):
    pass


schema = Schema(query=Query, mutation=Mutation)
