# Gesture-Based Robotic Control System

## Overview
This project implements a gesture-based control system for a robotic car using computer vision and machine learning. The system captures hand gestures using a webcam, processes them using MediaPipe, and translates the gestures into commands sent via Bluetooth to control the robot.

## Features
- **Hand Gesture Recognition**: Uses MediaPipe to detect and track hand movements.
- **Dataset Collection**: Captures hand angles and gestures for training.
- **Real-Time Processing**: Converts gestures into commands dynamically.
- **Bluetooth Communication**: Sends movement commands to the robot wirelessly.
- **Customizable Gestures**: Users can train the system with different gestures.

## Technologies Used
- **Python**
- **OpenCV** (for video processing)
- **MediaPipe** (for hand tracking)
- **NumPy** (for angle calculations)
- **Serial Communication** (for Bluetooth connection)

## Installation
### Prerequisites
Ensure you have Python installed. Then, install the required dependencies:
```sh
pip install opencv-python mediapipe numpy pyserial
```

### Hardware Requirements
- A webcam (for gesture recognition)
- Arduino with an HC-05 Bluetooth module
- A robotic car (configured to receive serial commands)

## Challenges Encountered
- **Gesture Detection Accuracy**: Improved by refining angle calculations.
- **Real-Time Processing**: Optimized by using efficient libraries.
- **Bluetooth Connectivity**: Resolved by configuring correct baud rates.
- **Data Collection**: Ensured variety in hand positions for better recognition.

## Future Improvements
- Implementing a machine learning model for advanced gesture recognition.
- Enhancing Bluetooth reliability for smoother communication.
- Adding a GUI for an improved user experience.

## Contributors
- **Ali Najma Mahamud**
- **Godish Kimberly**
- **Kibuku Carole June Wanjiku**
- **Priscilla Alakara**
- **Nicole Marwa Okello**

## License
This project is open-source and available under the MIT License.

