from flask import Flask, jsonify, render_template, send_from_directory
import pyzed.sl as sl
import threading
import time
import datetime  
import os

app = Flask(__name__)

zed = sl.Camera()
recording = False

def read_output_directory_path():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, 'absolute_output_directory_path.txt')
    with open(file_path, 'r') as file:
        return file.read().strip()

absolute_output_directory_path = read_output_directory_path()

def init_camera():
    # refer to https://www.stereolabs.com/docs/video/camera-controls for initailizing parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD1080
    init_params.depth_mode = sl.DEPTH_MODE.NEURAL
    init_params.camera_fps = 30
    init_params.coordinate_units = sl.UNIT.METER
    if zed.open(init_params) != sl.ERROR_CODE.SUCCESS:
        return False
    return True

def start_recording():
    global recording
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    svo_filename = f"{absolute_output_directory_path}{current_datetime}.svo"
    # note: compression modes for ZED are H265, H264, LOSSY, and LOSSLESS
    # refer to https://www.stereolabs.com/docs/video/recording if you want to change the compression mode!
    recording_parameters = sl.RecordingParameters(video_filename=svo_filename, compression_mode=sl.SVO_COMPRESSION_MODE.H264)
    if zed.enable_recording(recording_parameters) == sl.ERROR_CODE.SUCCESS:
        recording = True
        while recording:
            if zed.grab() != sl.ERROR_CODE.SUCCESS:
                break
            time.sleep(0.02)
    zed.disable_recording()

@app.route('/start', methods=['GET'])
def start():
    global recording
    if not recording:
        if not init_camera():
            return jsonify({'status': 'error', 'message': 'Failed to initialize camera!'}), 500
        threading.Thread(target=start_recording).start()
        return jsonify({'status': 'success', 'message': 'Recording started!'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Recording is already in progress!'}), 400

@app.route('/stop', methods=['GET'])
def stop():
    global recording
    if recording:
        recording = False
        zed.close()
        return jsonify({'status': 'success', 'message': 'Recording stopped!'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Recording is not in progress!'}), 400

@app.route('/list_svo_files', methods=['GET'])
def list_svo_files():
    try:
        files = [f for f in os.listdir(absolute_output_directory_path) if f.endswith('.svo')]
        #for file in files:
            #print(file)
        return jsonify({'status': 'success', 'files': files}), 200
    except Exception as e:
        print(e)
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
@app.route('/delete_svo/<filename>', methods=['POST'])
def delete_svo(filename):
    try:
        os.remove(os.path.join(absolute_output_directory_path, filename))
        return jsonify({'status': 'success', 'message': f'{filename} deleted!'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/download_svo/<filename>', methods=['GET'])
def download_svo(filename):
    try:
        return send_from_directory(absolute_output_directory_path, filename, as_attachment=True)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
