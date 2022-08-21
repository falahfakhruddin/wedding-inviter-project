import pandas as pd
import json
import datetime

from flask import jsonify
from flask import current_app as app, request, redirect

from app.models.guest_models import GuestList, TemplateMessage
from app.api import blueprint
from app.api.helper import arcgis_integrator as ai


@blueprint.route('/backend/_message/<surname>')
def get_message(surname):

    group = request.args.get('group')

    template_message = TemplateMessage.objects(group=group).first()

    if template_message is None:
        template_message = TemplateMessage.objects(group="default").first()

    template_message = template_message["template"]

    template_message = template_message.format(username=surname, group=group)

    return jsonify({'template_message': template_message, "group": group})


@blueprint.route('/backend/message-generator/<surname>', methods=['GET'])
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
    df = pd.read_csv(file, sep=';', converters={'group': lambda x: str(x)})
    app.logger.info("data: {}".format(df))

    data_json = json.loads(df.to_json(orient='records'))

    for data in data_json:
        guest = GuestList(name=data['name'],
                          group=data['group'])
        guest.save()

    return jsonify({"status": 200, "message": "success"})


@blueprint.route('/backend/guest-list/_delete', methods=['DELETE'])
def delete_guest_list():
    guest = GuestList.objects
    guest.delete()

    return jsonify({"status": 200, "message": "success"})


@blueprint.route('/backend/message/_get', methods=['GET'])
def get_template_message():
    template = TemplateMessage.objects(name='template')
    temp_msg = ""
    for msg in template:
        temp_msg = msg['template']

    return jsonify({"template_message": temp_msg})


@blueprint.route('/backend/message/_edit', methods=['POST'])
def edit_template_message():

    update_message = request.json

    template = TemplateMessage.objects(group=update_message['group'])
    for msg in template:
        app.logger.info('Message template, {} with group {}!'.format(template, update_message['group']))
        msg.update(template=update_message['template_message'])

    return jsonify({"status": 200, "message": "success"})


@blueprint.route('/backend/message/_add', methods=['POST'])
def add_template_message():
    add_message = request.json

    template = TemplateMessage(group=add_message['group'], template=add_message['template_message'])
    template.save()

    return jsonify({"status": 200, "message": "success"})


@blueprint.route('/backend/guest/_update_shared_at', methods=['POST'])
def update_guest_shared_at():

    guest = request.json

    guests = GuestList.objects(name=guest['name'])
    wib_time = datetime.datetime.now() + datetime.timedelta(hours=7)  # add 7 hour for convert uct to wib

    app.logger.info('Guest, {} with name {}!'.format(guests, guest['name']))
    for guest in guests:
        app.logger.info('Guest, {} with name {}!'.format(guests, guest['name']))
        guest.update(shared_at=wib_time)

    return jsonify({"status": 200, "message": "success"})


@blueprint.route('/backend/arcgis/populate-data', methods=['POST'])
def populate_rsvp_to_dashboard():
    config_airtable = app.config['AIRTABLE']
    config_gis = app.config['GIS']

    app.logger.info('config airtable {}'.format(config_airtable))
    app.logger.info('config gis {}'.format(config_gis))

    df = ai.construct_df_from_airtable(config_airtable)
    ai.upload_data_to_arcgis(config_gis, df)

    return jsonify({"status": 200, "message": "success"})

