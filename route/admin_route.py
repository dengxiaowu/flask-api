from controllers.admin import Admin
from flask import Blueprint

bp = Blueprint('admin', __name__, url_prefix='/pyapi/admin/')


# 管理员模块===============================================
@bp.route('register', methods=['POST'])
def admin_register():
    return Admin().add_admin()


@bp.route('login', methods=['POST', 'GET'])
def admin_login():
    return Admin().admin_login()


@bp.route('logout', methods=['POST', 'GET'])
def admin_logout():
    return Admin().admin_logout()
