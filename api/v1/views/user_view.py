from flask import Blueprint, request, jsonify, make_response
from api.v1.models.user_model import UserModel

user_api = Blueprint('user_v1', __name__, url_prefix="/api/v1")


@user_api.route("/users", methods=['POST'])
def api_user_sign_up():
    user = request.get_json(force=True)
    # Make Sure Keys Exist
    if {"firstname", "lastname", "othername", "email", "phoneNumber", "passportUrl", "password"} <= set(user):
        validated_user_msg = UserModel(user=user).user_sign_up()
        if 'Invalid Data' in validated_user_msg:
            # Invalidated data
            return make_response(jsonify({"status": 400, "error": "Parsing Invalid Data ,Bad Request"}), 400)
        elif 'User Exists' in validated_user_msg:
            # Duplicate User not allowed
            return make_response(jsonify({"status": 409, "error": "User Already Exists"}), 409)
        else:
            return make_response(
                jsonify({"status": 201, "data": "{} Signed Up Successfully".format(validated_user_msg)}), 201)
    return make_response(jsonify({"status": 403, "error": "Invalid Request ,Missing Data"}), 403)
