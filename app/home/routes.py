# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from app.models.guest_models import GuestList, TemplateMessage
from flask import current_app as app, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from flask_mongoengine import Pagination
from app import db
from jinja2 import TemplateNotFound


@blueprint.route('/index')
@login_required
def index():
    print("root: {}".format(request.script_root))
    if not request.script_root:
        # this assumes that the 'index' view function handles the path '/'
        request.script_root = url_for('base_blueprint.route_default', _external=True)
        print("root: {}".format(request.script_root))
    return render_template('index_template.html', segment='index')


@blueprint.route('/guest-list/<int:page>')
@login_required
def get_data(page):

    group = request.args.get('group')

    app.logger.info("filter group: {}".format(group))

    if not request.script_root:
        # this assumes that the 'index' view function handles the path '/'
        request.script_root = url_for('base_blueprint.route_default', _external=True)

    if group is None:
        guest = GuestList.objects.paginate(page=page, per_page=20)
    else:
        group_guest = GuestList.objects(group=group)
        guest = group_guest.paginate(page=page, per_page=20)

    return render_template('index.html', guest=guest, group=group)


@blueprint.route('/rsvp-list')
@login_required
def get_rsvp():

    if not request.script_root:
        # this assumes that the 'index' view function handles the path '/'
        request.script_root = url_for('base_blueprint.route_default', _external=True)

    return render_template('rsvp.html')


@blueprint.route('/template-messaging/<int:page>')
@login_required
def get_template_message_page(page):

    if not request.script_root:
        # this assumes that the 'index' view function handles the path '/'
        request.script_root = url_for('base_blueprint.route_default', _external=True)

    template = TemplateMessage.objects.paginate(page=page, per_page=20)

    return render_template('template_messaging.html', template_messages=template)


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith( '.html' ):
            template += '.html'

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( template, segment=segment )

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500


# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  

