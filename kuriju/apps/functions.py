#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.template import Template, Context


def msg_render(msg):
    return Template(msg).render(Context())
