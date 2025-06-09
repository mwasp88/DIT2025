from flask import Flask, send_from_directory, request, jsonify
import os
import json
try:
    import serial
except ImportError:  # Serial not installed, runtime will fail if used
    serial = None

SERIAL_PORT = os.environ.get("SERIAL_PORT", "/dev/ttyUSB0")
SERIAL_BAUD = int(os.environ.get("SERIAL_BAUD", "9600"))
serial_conn = None

app = Flask(__name__, static_folder=".")


def get_serial_connection():
    """Initialise serial connection if possible."""
    global serial_conn
    if serial_conn is not None:
        return serial_conn
    if serial is None:
        return None
    try:
        serial_conn = serial.Serial(SERIAL_PORT, SERIAL_BAUD, timeout=1)
    except Exception as e:
        print(f"Could not open serial port {SERIAL_PORT}: {e}")
        serial_conn = None
    return serial_conn

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/serial_event', methods=['POST'])
def serial_event():
    data = request.get_json(force=True, silent=True)
    if not isinstance(data, dict):
        return jsonify({'status': 'error', 'message': 'Invalid JSON'}), 400
    ser = get_serial_connection()
    if ser:
        try:
            ser.write((json.dumps(data) + '\n').encode('utf-8'))
        except Exception as e:
            print(f'Error writing to serial port: {e}')
    else:
        print('Serial output:', json.dumps(data))
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
