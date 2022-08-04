

import json
import os
from boxsdk import BoxAPIException, Client
from flask import flash
from apps.config import Config
from flask_login import current_user
from apps import db

from apps.authentication.models import Jwt, Users

def get_demo_folder_id(client:Client)->str:
	jwt_rec = Jwt.query.filter_by(box_app_id = Config.JWT_PUBLIC_KEY_ID).first()

	if jwt_rec.box_demo_folder_id == None or jwt_rec.box_demo_folder_id == '0':
		return create_demo_folder(client)

	return jwt_rec.box_demo_folder_id

def get_file_list(client:Client)->list:
	demo_folder_id = get_demo_folder_id(client)

	files = client.folder(demo_folder_id).get_items()
	
	file_list = []
	for file in files:
		file_list.append(file.id)

	if len(file_list) == 0:
		upload_demo_files(client)

	return file_list


def create_demo_folder(client:Client)->str:

	# try to create the demo folder in root
	try:
		demo_folder_id = client.folder(0).create_subfolder(Config.DEMO_FOLDER_NAME).id
	except BoxAPIException as error:
		demo_folder_id = error.context_info['conflicts'][0]['id']

	jwt_rec = Jwt.query.filter_by(box_app_id = Config.JWT_PUBLIC_KEY_ID).first()
	jwt_rec.box_demo_folder_id = demo_folder_id
	db.session.commit()
	return demo_folder_id

def upload_demo_files(client:Client)->list:

	demo_folder_id = get_demo_folder_id(client)

	demo_folder = client.folder(demo_folder_id)
	
	path = Config.basedir+"/"+Config.ASSETS_ROOT+'/demo_files/'
	files = os.listdir(path)

	for file in files:
		print(os.path.join(path,file))
		try:
			demo_folder.upload(os.path.join(path,file))
		except BoxAPIException as error:
			pass

	files = client.folder(demo_folder_id).get_items()
	file_list = []

	for file in files:
		file_list.append(file.id)
	
	return file_list