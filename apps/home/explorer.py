from flask import render_template
from flask_login import current_user

def explorer(token):

    token = token
    rootFolderId = 0

    optionsSidebar = {
        'hasActivityFeed': True,
        'hasMetadata': True,
        'hasSkills': True,
        'hasVersions': True,
        'detailsSidebarProps': {
            'hasProperties': True,
            'hasNotices': True,
            'hasAccessStats': True,
            'hasClassification': True,
            'hasRetentionPolicy': True,
        },
    }

    optionsPreviewer = {
        'logoUrl': 'box',
        'contentSidebarProps': optionsSidebar,
    }

    optionsUploader = {
    }

    options = {
        'container': '.ui-element',
        'currentFolderId': rootFolderId,
        'logoUrl': 'box',

        'defaultView': 'files',
        'sortBy': 'name',
        'sortDirection': 'ASC',

        'canPreview': True,
        'canDownload': True,
        'canDelete': True,
        'canRename': True,
        'canUpload': True,
        'canCreateNewFolder': True,
        'canShare': True,
        'canSetShareAccess': True,

        'contentPreviewProps': optionsPreviewer,
        'contentUploaderProps': optionsUploader,

    }
    return render_template('home/explorer.html',
                           segment='explorer',
                           avatar_url=current_user.avatar_url,
                           token=token,
                           rootFolderId=rootFolderId,
                           options=options,
                           )

    # return render_template('explorer.html',active_page=active_page, token=token, rootFolderId=rootFolderId, options=options)
