# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present [Box](https://developer.box.com/)
"""


import json

from apps.authentication.box_jwt import jwt_check_client, jwt_downscoped_access_token_get
from apps.authentication.models import Users
from apps.home import blueprint
from flask import request
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound
from apps.home.demo_files import get_demo_folder_id, get_file_list
from apps.home.explorer import explorer
from apps.home.previewer import previewer
from apps.home.picker import picker
from apps.home.uploader import uploader



@blueprint.route('/index')
@login_required
def index():
    return explorer(token=jwt_downscoped_access_token_get())
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

    return explorer(token=jwt_downscoped_access_token_get())    

@blueprint.route('/uploader')
@login_required
def page_uploader():

    demo_folder_id = get_demo_folder_id(jwt_check_client())
    return uploader(token=jwt_downscoped_access_token_get(),folder_id = demo_folder_id)       

@blueprint.route('/previewer')
@login_required
def page_previewer():

    file_list = get_file_list(jwt_check_client())
    return previewer(token=jwt_downscoped_access_token_get(),file_list=file_list)

@blueprint.route('/picker')
@login_required
def page_picker():

    demo_folder_id = get_demo_folder_id(jwt_check_client())
    return picker(token=jwt_downscoped_access_token_get(),folder_id=demo_folder_id)   


