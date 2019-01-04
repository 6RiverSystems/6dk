from app import app

from app.plugins.translation_engine import decipher

@app.route('/wms/acknowledgement', methods=['POST'])
def receive_acknowledgement():
	payload = request.get_json(force=True) or {}
	unmasked_data = decipher(payload, "acknowledgement")
	#send northbound
	#respond to fs
	return


@app.route('/wms/container-accepted', methods=['POST'])
def receive_container_accepted():
	#unmask fields
	#save to database
	#send northbound
	return


@app.route('/wms/print-request', methods=['POST'])
def receive_print_request():
	#unmask fields
	#save to database
	#send northbound
	return


@app.route('/wms/container-inducted', methods=['POST'])
def receive_container_inducted():
	#unmask fields
	#save to database
	#send northbound
	return


@app.route('/wms/pick-task-picked', methods=['POST'])
def receive_pick_task_picked():
	#unmask fields
	#save to database
	#send northbound
	return


@app.route('/wms/container-pick-complete', methods=['POST'])
def receive_container_pick_complete():
	#unmask fields
	#save to database
	#send northbound
	return


@app.route('/wms/container-taken-off', methods=['POST'])
def receive_container_taken_off():
	#unmask fields
	#save to database
	#send northbound
	return