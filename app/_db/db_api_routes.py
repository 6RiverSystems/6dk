from flask import jsonify, request

from app import app, logger
from app._db.db_maps import get_maps, get_table


@app.route('/db/list', methods=['GET'])
def db_home():
    return jsonify([
        {'count': db_table['table'].query.count(),
         'name': db_table['name']}
        for db_table in sorted(get_maps(), key=lambda k: k['name'])])


@app.route('/db/<table>', methods=['GET'])
def db_get_elements(table):
    logger.info('DB receiving request to list {}'.format(table))
    page = request.args.get('page', 1, type=int)
    per_page = app.config['ELEMENTS_PER_PAGE']
    db_table = get_table(table)
    if db_table:
        data = db_table.to_collection_dict(
            db_table.query.order_by(db_table.updated.asc()),
            page,
            per_page,
            'db_get_elements',
            table
        )
        return jsonify(data)
    else:
        return jsonify({'error': 'cannot query {}'.format(table)}), 400
