from flask import Blueprint, render_template

contacts_blueprint = Blueprint('contacts', __name__, template_folder='templates')


@contacts_blueprint.route('/contacts')
def contacts():
    return render_template('contacts/contacts.html')