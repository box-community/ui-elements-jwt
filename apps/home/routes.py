# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import json

from boxsdk import BoxAPIException
from apps.authentication.models import Users
from apps.home import blueprint
from flask import flash, render_template, request
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound
from apps.authentication.box_oauth import access_token_get, box_client, downscoped_access_token_get
from apps.home.explorer import explorer
from apps.home.previewer import previewer
from apps.home.picker import picker
from apps.home.uploader import uploader


@blueprint.route('/index')
@login_required
def index():
    return explorer(token=downscoped_access_token_get())
    # return render_template('home/index.html', segment='index',avatar_url=current_user.avatar_url)

@blueprint.route('/event/', methods=['POST'])
def event():
    request_data = request.get_json()
    print('***********************************************************')
    print(request_data)
    print('***********************************************************')
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@blueprint.route('/explorer')
@login_required
def page_explorer():

    return explorer(token=downscoped_access_token_get())    

@blueprint.route('/uploader')
@login_required
def page_uploader():
    user = Users.query.filter_by(id=current_user.id).first()
    folder_id = user.box_demo_folder_id
    client = box_client()

    if folder_id is None:
        flash('Demo folder not found, all uploads will be done in the root folder. To avoid this, go to settings and initialize the demo', 'alert-warning')
        return uploader(token=downscoped_access_token_get(),folder_id = 0)
    
    try:
        folder_id = client.folder(folder_id).get().id
    except BoxAPIException: 
        # the folder does not exist
        flash('Demo folder not found, all uploads will be done in the root folder. To avoid this, go to settings and initialize the demo', 'alert-warning')
        return uploader(token=downscoped_access_token_get(),folder_id = 0)

    return uploader(token=downscoped_access_token_get(),folder_id = folder_id)       

@blueprint.route('/previewer')
@login_required
def page_previewer():

    return previewer(token=downscoped_access_token_get())   

@blueprint.route('/picker')
@login_required
def page_picker():

    return picker(token=downscoped_access_token_get())   

