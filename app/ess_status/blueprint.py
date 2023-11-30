""" ESS Status """
from flask import Blueprint

from app.ess_status.ess_cal import ess_cal_bp

ess_status = Blueprint('ess', __name__, url_prefix='/ess')


ess_status.register_blueprint(ess_cal_bp)

