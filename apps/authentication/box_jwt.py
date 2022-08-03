from datetime import datetime, timedelta
from apps.authentication.cypto import decrypt_token, encrypt_token
from apps.authentication.models import Jwt
from apps.config import Config
from apps import db
from boxsdk import Client, JWTAuth

def jwt_test_from_file():

    access_token = jwt_access_token_get()
    print(f'Access token: {access_token}')
    

def jwt_test_manual():
    auth = JWTAuth(
        client_id       = Config.JWT_CLIENT_ID,
        client_secret   = Config.JWT_CLIENT_SECRET,
        enterprise_id   = Config.JWT_ENTERPRISE_ID,
        jwt_key_id      = Config.JWT_PUBLIC_KEY_ID,

        rsa_private_key_file_sys_path   = Config.private_key_path,
        rsa_private_key_passphrase      = Config.JWT_PASSPHRASE,
        
        store_tokens = jwt_store_token,
    )

    access_token = auth.authenticate_instance()

    client = Client(auth)
    service_account = client.user().get()

    print(f'Service Account user ID is {service_account.id}')
    print(f'Access token: {access_token}')


def jwt_access_token_get()->str:
    """
    Get the access token for the JWT assertion
    """

    # check if we have a valid access token
    jwt_rec = Jwt.query.filter_by(box_app_id = Config.JWT_PUBLIC_KEY_ID).first()

    if jwt_rec_is_valid(jwt_rec):
        return decrypt_token(jwt_rec.access_token)

    # get a new access token
    auth = JWTAuth.from_settings_file(Config.jwt_path,store_tokens=jwt_store_token)
    return auth.authenticate_instance()

def jwt_rec_is_valid(jwt_rec:Jwt)->bool:
    """
    Check if the JWT record is valid
    """
    if jwt_rec == None:
        return False
    
    if jwt_rec.expires_on < datetime.now():
        return False
        
    return True
    

def jwt_store_token(access_token:str, refresh_token:str = None)->bool:
    """
    Store the access tokens for the jwt app user
    """
    print(f'Storing access token: {access_token}')
    jwt_rec = Jwt.query.filter_by(box_app_id = Config.JWT_PUBLIC_KEY_ID).first()

    if jwt_rec == None:
        seconds=int(Config.JWT_EXPIRATION_SECONDS)
        jwt_new = Jwt(box_app_id = Config.JWT_PUBLIC_KEY_ID,
                        access_token = encrypt_token(access_token),
                        user_id = None,
                        expires_on = datetime.now() + timedelta(seconds=seconds),
        )
        db.session.add(jwt_new)
        db.session.commit()
        print(f'JWT Rec: {jwt_new}')
    else:
        jwt_rec.box_app_id = Config.JWT_PUBLIC_KEY_ID
        jwt_rec.access_token = encrypt_token(access_token)
        jwt_rec.user_id = None
        jwt_rec.expires_on = datetime.now() + timedelta(seconds=seconds)

        db.session.commit()
        print(f'JWT Rec: {jwt_rec}')

def jwt_downscoped_access_token_get(client:Client)->str:
    """
    Get the downscoped access token for the jwt app user
    """
 
    scope = ['base_explorer', 'item_preview', 'item_download', 'item_rename', 'item_share', 'item_delete',
             'base_picker', 'item_upload', # , 'item_share'
             'base_preview', 'annotation_edit', 'annotation_view_all', 'annotation_view_self', #, 'item_download'
             'base_sidebar', 'item_comment', #'item_task', # , 'item_rename', 'item_upload'
             'base_upload'
             ]

    downscoped_token = client.downscope_token(scopes=scope)
    return downscoped_token.access_token

