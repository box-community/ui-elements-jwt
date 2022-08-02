from flask import render_template
from flask_login import current_user


def uploader(token, folder_id=0, isPopup=False):
    token = token
    folder_id = folder_id

    if isPopup:
        modal = {
            'buttonLabel': 'Open modal to upload your files',
            'buttonClassName': 'btn-primary',
            'modalClassName': 'upload-modal',
            'overlayClassName': 'upload-overlay',
        }
    else:
        modal = None

    options = {
        'container': '.ui-element',
        'fileLimit': 100,

        'modal': modal,
    }

    return render_template('home/uploader.html',
                           segment='uploader',
                           avatar_url=current_user.avatar_url,
                           isPopup=isPopup,
                           token=token,
                           folder_id=folder_id,
                           options=options
                           )
