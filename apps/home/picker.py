from flask import render_template
from flask_login import current_user


def picker(token: str, folder_id=0, isPopup: bool = False, isPdf: bool = False):
    token = token
    folder_id = folder_id

    if isPopup:
        modal = {
            'buttonLabel': 'Open modal to select your files',
            'buttonClassName': 'btn-primary',
            'modalClassName': 'picker-modal',
            'overlayClassName': 'picker-overlay',
        }
    else:
        modal = None

    if isPdf == 'picker-pdf':
        extensions = ['pdf']
    else:
        extensions = []

    options = {
        'container': '.ui-element',

        'sortBy': 'name',
        'sortDirection': 'ASC',

        'logoUrl': 'box',
        'defaultView': 'files',

        'chooseButtonLabel': 'Choose',
        'cancleButtonLabel': 'Cancel',


        'extensions': extensions,

        'maxSelectable': 10,

        'canUpload': True,
        'canShareAccess': True,
        'canCreateNewFolder': True,

        'modal': modal,
    }

    return render_template('home/picker.html',
                           segment = 'picker',
                           avatar_url=current_user.avatar_url,
                           isPopup = isPopup,
                           token = token,
                           folder_id = folder_id,
                           options = options
                           )
