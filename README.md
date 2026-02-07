
# ♻️ Smart Waste Management System

A smart, IoT-enabled waste monitoring and forecasting system designed to improve urban cleanliness by automating waste level detection, optimizing collection routes, and predicting future waste patterns using machine learning.

---

## 📖 Overview

Traditional waste management systems often rely on manual checks and fixed collection schedules, leading to inefficiencies like overflowing bins or unnecessary trips. Our system addresses this by:

- Using ultrasonic sensors and NodeMCU for real-time bin monitoring.
- Displaying fill levels on a web dashboard.
- Applying ML models for waste forecasting.
- Providing route optimization to reduce fuel usage and time.
- Offering a mobile interface for collectors/admins.

---

## 🧠 Key Features

✅ Real-time bin level monitoring  
✅ Interactive data dashboard (web)  
✅ Machine Learning-based waste prediction  
✅ Collection route optimization  
✅ Mobile app for field usage (In Progress)  
✅ Firebase integration for real-time data  
✅ Solar-powered IoT setup for sustainability

---

## 🛠️ Tech Stack

| Layer        | Technologies Used                             |
|--------------|-----------------------------------------------|
| **IoT Layer**| NodeMCU ESP8266, HC-SR04 Ultrasonic Sensor     |
| **Backend**  | Flask / Node.js (REST API)                     |
| **Frontend** | HTML,Css,javascript, Chart.js                  |
| **Mobile App**| Flutter (In Future)                           |
| **Database** | Firebase                                       |
| **ML Tools** | Python (NumPy, Pandas, scikit-learn)           |
| **Others**   | Wi-Fi, Solar Panel, Lithium-ion Battery        |


## 🛠 Hardware Requirements
* **Microcontroller:** NodeMCU ESP8266
* **Sensors:** 2x HC-SR04 Ultrasonic Sensors
* **Power:** Micro-USB cable (5V)
* **Jumper Wires:** Male-to-Female & Male-to-Male
* **Breadboard**

---

## 🔌 Wiring Diagram

| HC-SR04 (Sensor) | NodeMCU Pin |
| :--- | :--- |
| **Bin 1: Trig** | D5 |
| **Bin 1: Echo** | D6 |
| **Bin 2: Trig** | D7 |
| **Bin 2: Echo** | D8 |
| **VCC** | Vin (5V) or 3V3 |
| **GND** | GND |



---

## 💻 Software Setup

### 1. Arduino IDE Configuration
1. Open Arduino IDE and go to **File > Preferences**.
2. Add this URL to "Additional Boards Manager URLs": 
   `http://arduino.esp8266.com/stable/package_esp8266com_index.json`
3. Go to **Tools > Board > Boards Manager**, search for `esp8266`, and install.
4. Install the following libraries via **Library Manager**:
   * `Firebase ESP8266 Client`
   * `ESP8266WiFi`

### 2. Firebase Configuration
1. Create a project in the [Firebase Console](https://console.firebase.google.com/).
2. Create a **Realtime Database** in `asia-southeast1` (or your preferred region).
3. Enable **Email/Password** authentication under the "Build > Authentication" tab.
4. Copy your **API Key** and **Database URL** into the code.

---

## 📊 Data Flow

1. **Sensing:** Ultrasonic sensors measure the distance from the lid to the trash.
2. **Processing:** NodeMCU converts distance into a percentage ($100\%$ full = 2cm, $0\%$ full = 10cm).
3. **Transmission:** Data is pushed to Firebase via HTTPS.
4. **Visualization:** The Web Dashboard fetches JSON data from Firebase and updates the UI.

📫 Contact
Feel free to reach out for questions, collaborations, or feedback!

📧 izharjamali99@gmail.com

🌐(https://www.linkedin.com/in/izhar-jamali-910ba7198)



🎥 Demo Video
https://youtu.be/p2CYMQoJfwo



🙌 Acknowledgements

SZABIST Hyderabad Faculty for guidance

Open-source libraries and contributors

Firebase & Chart.js Documentation

Community examples of smart city projects

