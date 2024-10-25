import jwt
import config
from flask import jsonify

# Encode a particular token using JWT
def token_encoder(user_id):
    secret = config.JWT_SECRET
    return jwt.encode(payload={'user_id': user_id}, 
                      key=secret, algorithm='HS256')

# Decode and verify a given token
def token_decoder(token):
    secret = config.JWT_SECRET
    try:
        payload = jwt.decode(token, secret, verify=True, 
                             algorithms=['HS256'])
        return {'user_id' : payload['user_id']}
    except:
        return {"403 - Forbidden" : "You don't have permission to access this."}