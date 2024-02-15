# ZEDServer
This is a Flask web application designed to manage the recording and handling of SVO files from a ZED camera.

## Features
- Ask server to start and stop recordings with the ZED camera.
- List all recorded SVO files.
- Download a SVO files from server.
- Delete a SVO files on server.

## Setup

1. **Install Dependencies**
    ```bash
    # on an empty Anaconda environment
    cd this_folder
    conda install --file requirements.txt

    # wheels should be already in folder, but if things don's work, run:
    python get_python_api.py
    ```

2. **Set Up and Run the server**
    ```bash
    # open absolute_output_directory_path.txt and put in your absolute path to the output folder

    # example (windows):
    D:\ZED\SVOStorage\
    # example (linux):
    /home/username/ZED/SVOStorage/

    # then start the server
    python ZED_server.py
    ```

3. **Open the web app**
    ```bash
    # open a web browser and go to the ip address shown in terminal
    # example terminal output:
    Running on http://127.0.0.1:5000
    Running on http://192.168.1.xxx:5000  # use this one
    ```

## Troubleshooting
- Modify following block if you want to change camera recording settings:
    ```python
    init_params.camera_resolution = sl.RESOLUTION.HD1080
    init_params.depth_mode = sl.DEPTH_MODE.NEURAL
    init_params.camera_fps = 30
    init_params.coordinate_units = sl.UNIT.METER
    ```
- It takes time between when you press "Start Recording" and when the camera actually starts recording. It is normal to experience some delay.
- When typing in absolute_output_directory_path.txt, make sure to use the correct slashes for your OS. Also, make sure to include the trailing slash at the end of the path.
    