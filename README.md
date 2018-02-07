# graphene-permissions

**Permission system for graphene-django apps.**

[![Build Status](https://travis-ci.org/redzej/graphene-permissions.svg?branch=travis-config)](https://travis-ci.org/redzej/graphene-permissions)
[![PyPI version](https://badge.fury.io/py/graphene-permissions.svg)](https://badge.fury.io/py/graphene-permissions)
[![Coverage Status](https://coveralls.io/repos/github/redzej/graphene-permissions/badge.svg?branch=master)](https://coveralls.io/github/redzej/graphene-permissions?branch=master)


## Overview

DRF-inspired permission system based on classes for graphene-django. Allows easy customization of permission classes for
for queries and mutations.

At this moment, only relay is supported.


## Requirements

* Python 3.5+
* Django 2.0+
* graphene-django 2.0+

## Installation

Install using pip:

```commandline
pip install graphene-permissions
```

## Usage

To enforce permission system, add appropriate mixin and set attribute `permission_classes`.


```python
from django.db import models
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_permissions.mixins import AuthNode, AuthMutation, AuthFilter
from graphene_permissions.permissions import AllowAny, AllowAuthenticated, AllowStaff


class Pet(models.Model):
    name = models.CharField(max_length=32)
    race = models.CharField(max_length=64)
    


class PetNode(AuthNode, DjangoObjectType):
    permission_classes = (AllowAuthenticated,)

    class Meta:
        model = Pet
        filter_fields = ('name',)
        interfaces = (relay.Node,)

```



