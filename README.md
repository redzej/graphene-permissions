# graphene-permissions

**Permission system for graphene-django apps.**

[![Build Status](https://travis-ci.org/redzej/graphene-permissions.svg?branch=travis-config)](https://travis-ci.org/redzej/graphene-permissions)
[![PyPI version](https://badge.fury.io/py/graphene-permissions.svg)](https://badge.fury.io/py/graphene-permissions)
[![Coverage Status](https://coveralls.io/repos/github/redzej/graphene-permissions/badge.svg?branch=master)](https://coveralls.io/github/redzej/graphene-permissions?branch=master)


## Overview

DRF-inspired permission system based on classes for graphene-django. Allows easy customization of permission classes for
for queries and mutations.


## Requirements

* Python 3.5+
* Django 2.0+
* graphene-django 2.0+

## Installation

Install using pip:

```commandline
pip install graphene-permissions
```

## Example

To enforce permission system, add appropriate mixin and set attribute `permission_classes`.


```python
### models.py
from django.db import models


class Pet(models.Model):
    name = models.CharField(max_length=32)
    race = models.CharField(max_length=64)
```
```python
### schema.py
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_permissions.mixins import AuthNode
from graphene_permissions.permissions import AllowAuthenticated


class PetNode(AuthNode, DjangoObjectType):
    permission_classes = (AllowAuthenticated,)

    class Meta:
        model = Pet
        filter_fields = ('name',)
        interfaces = (relay.Node,)
```

## Docs

# Setting up permission check
For queries use `AuthNode` mixin and inherite from `AuthFilter` class.
```python
class AllowAuthenticatedPetNode(AuthNode, DjangoObjectType):
    permission_classes = (AllowAuthenticated,)

    class Meta:
        model = Pet
        filter_fields = ('name',)
        interfaces = (relay.Node,)


class AllowAuthenticatedFilter(AuthFilter):
    permission_classes = (AllowAuthenticated,)


class PetsQuery:
    user_pet = relay.Node.Field(AllowAuthenticatedPetNode)
    all_user_pets = AllowAuthenticatedFilter(AllowAuthenticatedPetNode)
```

For mutations use `AuthMutation` mixin.
```python
class AddPet(AuthMutation, ClientIDMutation):
    permission_classes = (AllowAny,)
    pet = graphene.Field(AllowAnyPetNode)

    class Input:
        name = graphene.String()
        race = graphene.String()
        owner = graphene.ID()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        if cls.has_permission(root, info, input):
            owner = User.objects.get(pk=from_global_id(input['owner'])[1])
            pet = Pet.objects.create(name=input['name'], race=input['race'], owner=owner)
            return AddPet(pet=pet)
        return AddPet(pet=None)
        
class PetsMutation:
    authenticated_add_pet = AuthenticatedAddPet.Field()
```

# Customizing permission classes
Default permission classes are: `AllowAny`, `AllowAuthenticated`, `AllowStaff`.
