from flask import Blueprint, jsonify

test_bp = Blueprint('test', __name__)

@test_bp.route('/hello', methods=['GET'])
def hello():
    return jsonify({"message": "API 服务已启动"})
