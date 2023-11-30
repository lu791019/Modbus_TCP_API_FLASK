from flask import Blueprint, jsonify, request, make_response
from app.logger import logger
import json

def process_json(data):
    result = {}
    for key, value in data.items():
        if isinstance(value, dict):
            result[key] = process_json(value)

        else:
            # 在這裡可以添加你想要的轉換邏輯
            result[key] = round(value * 1, 1) if isinstance(value, (int, float)) else value
    return result


ess_cal_bp = Blueprint("ess_cal", __name__, url_prefix='/ess_cal')

@ess_cal_bp.route('/ess_status', methods=['POST'])
def ess_status():
    """
        ESS
        ---
        tags:
            - ESS Sata
        parameters:
          - name: params
            in: body
            required: true
            schema:
                type: object
                required: true
                properties:
                    file:
                        type: string
        produces: application/json
        responses:
            200:
                description: success
                schema:
                id: Result
                properties:
                    message:
                    type: string
                    default: {'msg': 'ess status data upload success'}
    """
    try:

        # if file is None:
        #     return jsonify({"error": "file is required"}), 400

        # if ',' in file:
        #     file_type, file = file.split(',')
        # else:
        #     file_type = ''
        #     file = ''

        # with open('ess_status_data_test.json', 'r') as json_file:
        #     ess_status_data = json.load(json_file)
        ess_status_data = request.get_json()

        if not ess_status_data:
            return jsonify({"error": "Invalid JSON data"}), 400

        result =  {
            # "productName": "testName",
            "productName": ess_status_data['productName'],
            "eticaBMS": process_json(ess_status_data['eticaBMS']),
            "danfossPCS": process_json(ess_status_data['danfossPCS']),
            "dieselGenerator": process_json(ess_status_data['dieselGenerator'])
            }
        # result = OrderedDict([
        #         ("testName", ess_status_data.get('productName', '')),
        #         ("eticaBMS", process_json(ess_status_data.get('eticaBMS', {}))),
        #         ("danfossPCS", process_json(ess_status_data.get('danfossPCS', {}))),
        #         ("dieselGenerator", process_json(ess_status_data.get('dieselGenerator', {})))
        #     ])

        return jsonify(result)


    except Exception as error:  # pylint: disable=broad-except
        logger.exception('Exception ERROR => %s', str(error))
        return make_response({"error": str(error)}, 400)
