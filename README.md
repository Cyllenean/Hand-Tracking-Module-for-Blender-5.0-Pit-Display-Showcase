# CYLLENEAN - Hand Tracking Module for Blender 5.0+ (Pit Display)

A gesture-controlled 3D object manipulator for Blender, built for our STEM Racing team's pit display showcase. Visitors can manipulate a 3D model of our car using hand gestures in front of a webcam — no keyboard or mouse needed.

The model in the scene is our STEM Racing car, remeshed using QRemeshify for a cleaner wireframe view. Note that this does not represent the final version of the car.

## Features

- **Blender 5.0+ Compatible** — Uses modern Blender Python APIs (timer-based updates instead of blocking loops)
- **Real-time Hand Tracking** — MediaPipe detects hand landmarks through a webcam
- **Gesture Controls** — Scale, rotate, and pan the 3D model with simple hand poses
- **Enhanced Pan Sensitivity** — Object moves noticeably with small hand movements (though still buggy)
- **Scale Preservation** — Scale value is preserved across rotation and panning
- **Configurable Sensitivity** — Easy-to-tweak values for scale, rotate, and pan

## Requirements

- Blender 2.8 or newer (only Blender 5.0 + has been tested)
- Python 3.10–3.12
- Webcam
- Python packages: `opencv-python`, `mediapipe`, `numpy`
- Current version only natively supports Windows 10/11

## Installation

1. Clone this repository or Download the files manually:
   ```bash
   git clone https://github.com/Cyllenean/Hand-Tracking-Module-for-Blender-5.0-Pit-Display-Showcase.git
   cd Hand-Tracking-Module-for-Blender-5.0-Pit-Display-Showcase

2. Install Python dependencies:
    ```bash
    pip install -r requirements.txt

3. Open the Blender file

4. In Blender's Text Editor, update the new_path variable in the script to point to your src folder.

5. Run the Blender script (Alt+P or click Run Script).

6. In a separate terminal, run:
    ```bash
    cd 'your_file_path'
    python main.py

7. Make sure your webcam shutter is off/not covered.


## Changes from the Original

This project is a fork of an existing hand-tracking project, heavily modified for our pit display use case. Key changes include:

1. Blender Script: Replaced Blocking Loop with Timer
Original: An infinite while True loop froze Blender completely, causing the screen to turn white.

Fix: Replaced with Blender's built-in timer system:

python
def update_object_from_files():
    # ... read and apply values

def timer_update():
    update_object_from_files()
    return 0.05  # Run again after 0.05 seconds

bpy.app.timers.register(timer_update, first_interval=0.05)
2. Blender Script: Fixed Fullscreen API Call
Original: On Blender 4.x and 5.x, the fullscreen call raised ValueError: 1-2 args execution context is supported because the operator signature changed.

Fix: Removed the problematic fullscreen call entirely.

3. Blender Script: Corrected File Path Handling
Original: The path was hardcoded to the original author's drive, and the variable was written as a literal string ("new_path\\scale.txt"), causing FileNotFoundError on every other machine.

Fix: Used os.path.join() with a single user-editable new_path variable.

4. Blender Script: Incremental Rotation
Original: obj.rotation_euler[2] = rotation_angle_radians snapped the object to a fixed angle every frame.

Fix: Changed to += so rotation accumulates smoothly.

5. Python Script: Increased Rotation Sensitivity
Original: rd = 1 made rotation values range from only -1 to 1 degree — invisible in Blender.

Fix: Raised rd to a visible value.

6. Python Script: Preserved Scale Across Gestures
Original: Every rotation or pan gesture reset scale.txt to "1.0", shrinking the object.

Fix: Introduced a current_scale variable that stores the last scale value and writes it back during other gestures.

7. Python Script: Higher Pan Sensitivity
Original: Pan range was too small to be noticeable.

Fix: Increased x_blend and z_blend, and applied a multiplier.

8. Compatibility: MediaPipe Version
Problem: MediaPipe 0.10.31+ removed the legacy mp.solutions API that the original code depends on, causing AttributeError: module 'mediapipe' has no attribute 'solutions'.

Fix: Pinned MediaPipe to 0.10.8 in requirements.txt


## Credits

This project is a fork of IronHands by akgupta1337, which provided the original hand-tracking framework, gesture mapping, and Blender integration. The original project is licensed under the MIT License.

The 3D car model included was remeshed using QRemeshify.


---

## License

Released under the **MIT License**. See `LICENSE` for details.

You are free to use, modify and redistribute this tool, including for commercial purposes, provided the copyright notice and licence text are retained. Attribution is appreciated but not required.

---

## Contact

**Team Cyllenean**
Australian International School Hong Kong
3A Norfolk Road, Kowloon Tong, Kowloon, Hong Kong

- Email: [cyllenean.aishk@gmail.com](mailto:cyllenean.aishk@gmail.com)
- Instagram: [@cyllenean](https://www.instagram.com/cyllenean/)
- LinkedIn: [Team Cyllenean](https://www.linkedin.com/in/team-cyllenean-5725653b0/)
- GitHub: [github.com/Cyllenean](https://github.com/Cyllenean)

---

<p align="center">
  <strong>Speed · Precision · Minimalism</strong><br>
  Copyright © 2026 Cyllenean. All Rights Reserved.
</p>
