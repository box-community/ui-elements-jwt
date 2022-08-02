

import json
import os
from boxsdk import BoxAPIException
from apps.config import Config
from flask_login import current_user
from apps.authentication.box_oauth import box_client
from apps import db

from apps.authentication.models import Users


def init_files():
    pass

def create_demo_folder():

	client = box_client()

	# try to create the demo folder in root
	try:
		demo_folder_id = client.folder(0).create_subfolder(Config.DEMO_FOLDER_NAME)
	except BoxAPIException as error:
		demo_folder_id = error.context_info['conflicts'][0]['id']

	user = Users.query.filter_by(id=current_user.id).first()
	user.box_demo_folder_id = demo_folder_id
	db.session.commit()

def upload_demo_files():
	user = Users.query.filter_by(id=current_user.id).first()
	demo_folder_id = user.box_demo_folder_id
	client = box_client()
	demo_folder = client.folder(demo_folder_id)
	
	path = Config.basedir+"/"+Config.ASSETS_ROOT+'/demo_files/'
	files = os.listdir(path)

	for file in files:
		print(os.path.join(path,file))
		try:
			demo_folder.upload(os.path.join(path,file))
		except BoxAPIException as error:
			pass