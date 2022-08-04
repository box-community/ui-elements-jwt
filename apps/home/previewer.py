from boxsdk import BoxAPIException
from flask import flash, render_template, session
from flask_login import current_user
from apps.authentication.box_jwt import jwt_client
from apps.authentication.models import Users
from apps.config import Config


def previewer(token:str,file_list:list):

    file_id = file_list[0]

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
