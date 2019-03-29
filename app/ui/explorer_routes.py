from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from app import app, rule
from app.ui._forms import ExplorerMessage


@app.route('/explorer', methods=['GET'])
@login_required
def explorer_main():
    profile = current_user.get_active_profile()
    if profile:
        messages = [{
            'name': message,
            'form': render_template('embedded_form.html',
                                    form=ExplorerMessage(),
                                    formname='{}'.format(message),
                                    action='#',
                                    id='post-{}'.format(message))
        }
            for message in rule.get_messages_list('southbound')]
        return render_template('explorer/explorer_main.html',
                               messages=messages,
                               profile=profile,
                               header='Explorer',
                               )
    else:
        flash('You must activate a profile before using Explorer.')
        return redirect(url_for('profiles_main'))
