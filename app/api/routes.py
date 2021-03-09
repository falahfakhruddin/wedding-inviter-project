import pandas as pd
import json

from flask import jsonify
from flask import current_app as app, request, redirect

from app.models.guest_models import GuestList
from app.api import blueprint


@blueprint.route('/backend/message-generator/template/<surname>', methods=['GET'])
def message_generator(surname):

    phone = request.args.get('phone')
    invitation_code = request.args.get('invitation_code')

    template_message = "Halo {} coba buka ini ya https://sanfalstory.wedew.id/{}".format(surname, invitation_code)

    url = "https://wa.me/{}?text={}".format(phone, template_message)

    app.logger.info("wa url: {}".format(url))
    return redirect(url, code=302)


@blueprint.route('/backend/guest-list/_upload', methods=['POST'])
def upload_csv():
    file = request.files['file']
    app.logger.info("file: {}".format(file))
    df = pd.read_csv(file, sep=';', converters={'invitation_code': lambda x: str(x)})
    app.logger.info("data: {}".format(df))

    data_json = json.loads(df.to_json(orient='records'))

    for data in data_json:
        guest = GuestList(invitation_code=data['invitation_code'],
                          name=data['name'],
                          group=data['group'],
                          phone=data['phone'])
        guest.save()

    return jsonify({"status": 200, "message": "success"})


@blueprint.route('/backend/guest-list/_delete', methods=['DELETE'])
def delete_guest_list():
    guest = GuestList.objects
    guest.delete()

    return jsonify({"status": 200, "message": "success"})

