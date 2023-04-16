import os

def set_up_local_oauth():
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'