from boxsdk import BoxAPIException
from flask import flash, render_template, session
from flask_login import current_user
from apps.authentication.box_oauth import box_client
from apps.authentication.models import Users
from apps.config import Config


def previewer(token: str):
    token = token
    user = Users.query.filter_by(id=current_user.id).first()

    client = box_client()

    try:
        files = client.folder(user.box_demo_folder_id).get_items()
        file_list = []

        for file in files:
            file_list.append(file.id)

        file_id = file_list[0]

    except BoxAPIException:
        flash('No files found in the demo folder. Go to settings and initialize the demo', 'alert-warning')
        file_id = None

    contentSidebarProps = {
        'detailsSidebarProps': {
            'hasNotices': True,
            'hasProperties': True,
            'hasAccessStats': True,
            'hasVersions': True
        },
        'hasActivityFeed': True,
        'hasSkills': True,
        'hasVersions': True,
        'hasMetadata': True
    }

    options = {
        'container': '.ui-element',
        'header': 'light',
        'logoUrl': 'box',

        'collection': file_list,

        'hasHeader': True,
        'showAnnotations': False,
        'showDownload': True,

        'contentSidebarProps': contentSidebarProps,

    }

    isSingle = True if file_list.count == 1 else False

    return render_template('home/previewer.html',
                           segment='previewer',
                           avatar_url=current_user.avatar_url,
                           token=token,
                           file_id=file_id,
                           options=options,
                           isSingle=isSingle
                           )
