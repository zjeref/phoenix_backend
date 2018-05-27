from flask import Blueprint
from app import jsonify
from app.models import Subject
from app.utils import decorators

api = Blueprint('subject_api', __name__, url_prefix='/api/subject')


@api.route('/list', methods=['GET'])
@decorators.login_required
def list():
    subjects = [s.serialize() for s in Subject.query.all()]
    data = dict(status='success', subjects=subjects)
    return jsonify(data), 200
