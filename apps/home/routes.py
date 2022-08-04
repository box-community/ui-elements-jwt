# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import json

from boxsdk import BoxAPIException
from apps.authentication.box_jwt import jwt_auth, jwt_client, jwt_downscoped_access_token_get
from apps.authentication.models import Users
from apps.home import blueprint
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound
from apps.home.demo_files import create_demo_folder, get_demo_folder_id, get_file_list, upload_demo_files
from apps.home.explorer import explorer
from apps.home.previewer import previewer
from apps.home.picker import picker
from apps.home.uploader import uploader

auth = None
client = None

def check_client():
    global auth, client
    if auth is None:
        auth = jwt_auth()
    if client is None:
        client = jwt_client(auth)
    get_file_list(client)

@blueprint.route('/index')
@login_required
def index():
    check_client()

    return explorer(token=jwt_downscoped_access_token_get(client))
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
    check_client()
    return explorer(token=jwt_downscoped_access_token_get(client))    

@blueprint.route('/uploader')
@login_required
def page_uploader():
    check_client()
    demo_folder_id = get_demo_folder_id(client)

    if demo_folder_id is None or demo_folder_id == 0:
        flash('Demo folder not found, all uploads will be done in the root folder. To avoid this, go to settings and initialize the demo', 'alert-warning')
        return uploader(token=jwt_downscoped_access_token_get(client),demo_folder_id = 0)

    return uploader(token=jwt_downscoped_access_token_get(client),folder_id = demo_folder_id)       

@blueprint.route('/previewer')
@login_required
def page_previewer():
    check_client()
    file_list = get_file_list(client)

    return previewer(token=jwt_downscoped_access_token_get(client),file_list=file_list)

@blueprint.route('/picker')
@login_required
def page_picker():
    check_client()
    demo_folder_id = get_demo_folder_id(client)
    return picker(token=jwt_downscoped_access_token_get(client),folder_id=demo_folder_id)   

