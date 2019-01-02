from app import app


@app.route('/wms/acknowledgement', methods=['POST'])
def receive_acknowledgement():
	#unmask fields
	#save to database
	#send northbound
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