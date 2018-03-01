# graphene-permissions

**Permission system for graphene-django apps.**

[![Build Status](https://travis-ci.org/redzej/graphene-permissions.svg?branch=master)](https://travis-ci.org/redzej/graphene-permissions)
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

### Setting up permission check
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
class AuthenticatedAddPet(AuthMutation, ClientIDMutation):
    permission_classes = (AllowAuthenticated,)
    pet = graphene.Field(AllowAuthenticatedPetNode)

    class Input:
        name = graphene.String()
        race = graphene.String()
        owner = graphene.ID()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        if cls.has_permission(root, info, input):
            owner = User.objects.get(pk=from_global_id(input['owner'])[1])
            pet = Pet.objects.create(name=input['name'], race=input['race'], owner=owner)
            return AuthenticatedAddPet(pet=pet)
        return AuthenticatedAddPet(pet=None)

        
class PetsMutation:
    authenticated_add_pet = AuthenticatedAddPet.Field()
```

### Customizing permission classes
Default permission classes are: `AllowAny`, `AllowAuthenticated`, `AllowStaff`.
You can set up equal permission for both queries and mutations with one class, simply subclass one of these classes 
and to limit access for given object, override appropriate method. Remember to return `true` if user should be given 
access and `false`, if denied.

```python
class AllowMutationForStaff(AllowAuthenticated):
    @staticmethod
    def has_node_permission(info, id):
        # logic here 
        # return boolean
        
    @staticmethod
    def has_mutation_permission(root, info, input):
        if info.request.user.is_staff:
            return True
        return False
       
    @staticmethod
    def has_filter_permission(info):
        # logic here
        # return boolean
```

### Multiple permissions
You can set up multiple permissions checks, simply adding more classes. Permission is evaluated for every class.
If one of the checks fails, access is denied.

```python
class CustomPetNode(AuthNode, DjangoObjectType):
    permission_classes = (AllowAuthenticated, AllowStaff, AllowCustom)
    
    class Meta:
        model = Pet
        interfaces = (relay.Node,)
```
