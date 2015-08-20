# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2012, 2013, 2014, 2015 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""Implement redirection URLs."""

import inspect

from flask import Blueprint, abort, current_app, make_response, redirect, \
    render_template, request, url_for
from flask_login import current_user

from .api import get_redirection_data
from .registry import get_redirect_method

blueprint = Blueprint('goto', __name__, url_prefix="/goto",
                      template_folder='templates', static_folder='static')


@blueprint.route('/<path:component>', methods=['GET', 'POST'])
def index(component):
    """Handle /goto set of pages."""
    redirection_data = get_redirection_data(component)
    goto_plugin = get_redirect_method(redirection_data['plugin'])
    args, dummy_varargs, dummy_varkw, defaults = inspect.getargspec(
        goto_plugin)
    args = args and list(args) or []
    args.reverse()
    defaults = defaults and list(defaults) or []
    defaults.reverse()
    params_to_pass = {}
    for (arg, default) in zip(args, defaults):
        params_to_pass[arg] = default

    # Let's put what is in the GET query
    for key, value in request.args.items():
        if key in params_to_pass:
            params_to_pass[key] = str(value)

    # Let's override the params_to_pass to the call with the
    # arguments in the configuration
    configuration_parameters = redirection_data['parameters'] or {}
    params_to_pass.update(configuration_parameters)

    # Let's add default parameters if the plugin expects them
    if 'component' in params_to_pass:
        params_to_pass['component'] = component
    if 'path' in params_to_pass:
        params_to_pass['path'] = request.path
    if 'user_info' in params_to_pass:
        params_to_pass['user_info'] = current_user._get_current_object()
    if 'req' in params_to_pass:
        params_to_pass['req'] = request._get_current_object()
    try:
        new_url = goto_plugin(**params_to_pass)
    except Exception:
        current_app.logger.exception("Redirection handler problem.")
        abort(404)
    if new_url:
        if new_url.startswith('/'):
            new_url = current_app.config['CFG_SITE_URL'] + new_url
        return redirect(new_url)
    abort(404)
