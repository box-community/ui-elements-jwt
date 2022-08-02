
from flask import redirect
from flask_login import current_user, logout_user
from apps.authentication.cypto import decrypt_token, encrypt_token
from apps.config import Config
from apps import db,login_manager
from boxsdk import OAuth2, Client
from apps.authentication.models import Users


def get_authorization_url():
    """
    Get the authorization url for the user
    """
    user = Users.query.filter_by(id=current_user.id).first()

    #user must be logged in
    if user == None:
        return None,None

    oauth = OAuth2(
        client_id=Config.CLIENT_ID,
        client_secret=Config.CLIENT_SECRET,
    )

    auth_url, csrf_token = oauth.get_authorization_url(Config.REDIRECT_URI)

    if user:
        user.csrf_token = csrf_token
        db.session.commit()

    return auth_url, csrf_token

def authenticate(code:str) -> None:
    
    oauth = OAuth2(
        client_id=Config.CLIENT_ID,
        client_secret=Config.CLIENT_SECRET,
        store_tokens=store_tokens
    )
    oauth.authenticate(code)

def access_token_get()->str:
    """
    Get the access token for the current user
    """
    
    user = Users.query.filter_by(id=current_user.id).first()
    if user == None or user.access_token == None or user.refresh_token == None:
        return None

    access_token = decrypt_token(user.access_token)
    refresh_token = decrypt_token(user.refresh_token)
    oauth = OAuth2(client_id=Config.CLIENT_ID
                    , client_secret=Config.CLIENT_SECRET
                    , access_token=access_token
                    , refresh_token=refresh_token
                    , store_tokens=store_tokens
                    )
    
    # client = Client(oauth)

    try:
        
        # client.user().get() # this forces a refresh of the access token if it is 
        user = Users.query.filter_by(id=current_user.id).first()
        return decrypt_token(user.access_token)
    except:
        # if there is an error, we need to re authorize the app
        return None

def downscoped_access_token_get()->str:
    """
    Get the access token for the current user
    """
 
    client = box_client()
 
    scope = ['base_explorer', 'item_preview', 'item_download', 'item_rename', 'item_share', 'item_delete',
             'base_picker', 'item_upload', # , 'item_share'
             'base_preview', 'annotation_edit', 'annotation_view_all', 'annotation_view_self', #, 'item_download'
             'base_sidebar', 'item_comment', #'item_task', # , 'item_rename', 'item_upload'
             'base_upload'
             ]

    downscoped_token = client.downscope_token(scopes=scope)
    return downscoped_token.access_token


def store_tokens(access_token:str, refresh_token:str)->bool:
    """
    Store the access and refresh tokens for the current user
    """

    user = Users.query.filter_by(id=current_user.id).first()

    if user:
        user.access_token = encrypt_token(access_token)
        user.refresh_token = encrypt_token(refresh_token)
        db.session.commit()
        return True
    return False


def box_client() -> Client:
    """
    Get the box client for the current user
    """

    user = Users.query.filter_by(id=current_user.id).first()
    access_token = decrypt_token(user.access_token)
    refresh_token = decrypt_token(user.refresh_token)

    if user:
        oauth = OAuth2(client_id=Config.CLIENT_ID
                     , client_secret=Config.CLIENT_SECRET
                     , access_token=access_token
                     , refresh_token=refresh_token
                     , store_tokens=store_tokens
                     )

        # oauth.refresh(access_token)

        client = Client(oauth)
        
        try:
            client.user().get() # this should force a refresh of the access token
            return client
        except:
            # if there is an error, we need to re authorize the app
            return None
    return None

