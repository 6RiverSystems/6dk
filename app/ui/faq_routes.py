from flask import render_template, request, url_for, jsonify
from flask_login import login_required

from app import app
from app.plugins.faq_helper import get_faqs


@app.route('/faq', methods=['GET', 'POST'])
@login_required
def faq_main():
    query = request.args.get('q')
    faqs = get_faqs(request.method)
    if query:
        faqs = [faq for faq in faqs if query.lower() in str(faq).lower()]

    options = [
        {
            'linkname': faq['Q'],
            'meta_html': faq['A'],
        } for faq in faqs
    ]

    option_block = render_template('option_block.html',
                                   options=options, query=query,
                                   bold_text=True)
    if request.method == 'GET':
        return render_template(
            'options.html',
            option_block=option_block,
            search=url_for('faq_main'))
    else:
        return jsonify({'html': option_block})
