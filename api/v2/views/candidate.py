from flask import Blueprint, request, make_response, jsonify
from api.v2.models.candidate import CandidateModel
from flask_jwt_extended import jwt_required
from . import check_user, id_conversion

candidate_api_v2 = Blueprint('candidate_v2', __name__, url_prefix="/api/v2")


@candidate_api_v2.route("/office/<office_id>/register", methods=['POST'])
@jwt_required
def api_candidate_register(office_id):
    if 'Requires Admin Privilege' not in check_user():
        register_data = request.get_json(force=True)
        oid = id_conversion(office_id)
        if {'party', 'candidate'} <= set(register_data):
            cid = id_conversion(register_data['party'])
            pid = id_conversion(register_data['candidate'])
            if 'Invalid' not in [cid, pid, oid]:
                candidate_info = CandidateModel(oid, cid, pid).register_candidate()
                if isinstance(candidate_info, list):
                    return make_response(
                        jsonify(
                            {"status": 201, "data": [{"office": candidate_info[0][0], "user": candidate_info[0][2]}]}),
                        201)
                elif 'Candidate Conflict' in candidate_info:
                    return make_response(
                        jsonify({"status": 409, "error": "Candidate Already Registered or Doesnt Exist"}),
                        409)
                elif 'Empty' in candidate_info:
                    make_response(
                        jsonify({"status": 404, "data": "data not found"}),
                        201)
            return make_response(jsonify({"status": 400, "error": "Input of Invalid Id"}), 400)
        return make_response(jsonify({"status": 400, "error": "Missing Input Values"}), 400)
    return make_response(jsonify({"status": 401, "error": "Unauthorized Access,Requires Admin Rights"}), 401)


@candidate_api_v2.route("/office/<office_id>/register", methods=['GET'])
@jwt_required
def api_get_candidates(office_id):
    oid = id_conversion(office_id)
    candidates = CandidateModel().get_all_candidates_by_office(oid)
    if isinstance(candidates, list):
        candidates_list = []
        for candidate in candidates:
            candidate_dict = {
                "office": candidate[0],
                "party": candidate[1],
                "candidate name": candidate[2]
            }
            candidates_list.append(candidate_dict)

        return make_response(
            jsonify({"status": 200, "data": candidates_list}),
            200)
