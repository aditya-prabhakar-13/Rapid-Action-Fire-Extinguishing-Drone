# 🚁 Drone-Assisted Firefighting System

A full-stack project aiming to design, simulate, and deploy a **drone-based rapid response system** to assist firefighters during fire emergencies. The drone is capable of indoor navigation, fire detection, and initial suppression—acting as the first line of defense until firefighting teams arrive.

---

## 🔥 Project Overview

Fire emergencies require fast and intelligent response systems. This project combines simulation and real-world implementation to create an autonomous or semi-autonomous drone that can:

- Rapidly assess fire situations
- Navigate through indoor environments
- Detect and localize fire sources
- Provide real-time data to fire teams
- Execute localized fire suppression

---

## 🎯 Objectives

- 🕒 **Rapid Deployment**: Drone acts as a first responder.
- 📡 **Real-Time Monitoring**: Live video and telemetry feedback.
- 🧭 **Indoor Navigation**: Smart pathfinding around obstacles.
- 🔍 **Fire Detection**: Using thermal and vision-based sensors.
- 🧯 **Localized Fire Suppression**: With onboard extinguishing agents.

---

## 🧰 Tech Stack

| Component        | Technology / Tools              |
|------------------|----------------------------------|
| **Simulation**   | PyBullet / Gazebo / Unity        |
| **Control System** | ROS, PX4, MAVROS                 |
| **Hardware**     | Custom quadcopter frame, Pixhawk, LiDAR, IR sensor, thermal camera |
| **Fire Suppression** | CO₂ or dry chemical extinguisher module |
| **Navigation**   | SLAM, obstacle avoidance, PID control |
| **Languages**    | Python, C++, Bash                |

---

## 📁 Project Structure

```plaintext
📁 Drone-Firefighter
├── simulation/          # Simulation environment and scripts
│   ├── environment/     # PyBullet/Gazebo scene setup
│   ├── models/          # 3D models (walls, fire, furniture)
│   └── scripts/         # Python scripts to run simulations
│
├── hardware/            # Physical drone design, schematics, and firmware
│   ├── CAD/             # 3D drone design files
│   ├── schematics/      # Circuit diagrams and wiring
│   └── firmware/        # Flight controller and sensor firmware
│
├── software/            # Drone software stack
│   ├── navigation/      # Path planning and SLAM
│   ├── control/         # PID and flight control algorithms
│   └── telemetry/       # Data communication and ground station scripts
│
├── fire_detection/      # Fire recognition models and training data
│   ├── models/          # Pre-trained fire detection models
│   └── dataset/         # Fire and smoke image/video datasets
│
├── suppression_module/  # Control of fire extinguishing mechanisms
│   ├── actuator_control/ # Servo/motor-based control
│   └── sensors/         # Pressure, temperature, etc.
│
├── docs/                # Documentation and research papers
│   ├── design_docs/     # System design, flowcharts
│   └── references/      # External references and studies
│
└── README.md            # Project description
```
---

## 🚧 Current Progress

- [x] Concept Design & Architecture
- [ ] Simulation Environment Setup
- [ ] Fire Detection Algorithm
- [ ] Drone Hardware Assembly
- [ ] Fire Suppression Module Integration
- [ ] Autonomous Navigation Development
- [ ] Full System Integration & Testing

---

## 📸 Media

*(Add GIFs, videos, or images of simulation / prototype here)*

---

## 📝 How to Run the Simulation


# Clone the repository
```bash
git clone https://github.com/your-username/Drone-Firefighter.git
cd Drone-Firefighter/simulation
```

# Install dependencies (example: for PyBullet)
```bash
pip install pybullet
```
```bash
pip install pillow
```
- Install Anaconda

# Run the simulation
On Anaconda prompt
- 1) Create a python environment (say 'env')
- 2) Run following commands
```bash
conda activate env
```
```bash
env simul.py
