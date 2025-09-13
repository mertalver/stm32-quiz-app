# Embedded Calculator (Quiz Application)

An interactive quiz application on **STM32F411E-DISCO** with OLED
display, potentiometer-based difficulty control, and a Python (PyQt)
GUI.
The system generates random math questions, communicates over UART, and
provides real-time feedback using LEDs, OLED, and a desktop GUI.

------------------------------------------------------------------------

## ✨ Features
-   🔢 **Random Math Questions**: Addition, subtraction, multiplication,
    and division
-   🎚 **Difficulty Control**: Potentiometer input (Easy / Medium /
    Hard)
-   ⏱ **Time-Limited Answers**: Countdown depends on difficulty level
-   💡 **Real-Time Feedback**:
    -   ✅ Correct → Green LED + "DOGRU" on OLED
    -   ❌ Wrong → Red LED + correct answer displayed on OLED
    -   ⏳ Timeout → Orange LED + "SURENIZ BITTI"
-   📊 **Performance Tracking**: Correct / Wrong / Timeout stats
-   🖥 **Cross-Platform GUI**: Python (PyQt5 + PySerial + Qt Material)

------------------------------------------------------------------------

## 🛠 Hardware

-   STM32F411E-DISCO development board (ARM Cortex-M4)
-   OLED Display (SSD1306 via I²C)
-   Potentiometer (difficulty input via ADC)
-   On-board LEDs (feedback indicators)
-   USB (UART CDC communication)

------------------------------------------------------------------------

## 💻 Software

### Embedded Side (C / STM32CubeIDE)

-   **ADC**: Reads potentiometer values for difficulty selection
-   **Timer**: Handles countdown timing and interrupts
-   **UART (USB)**: Serial communication with the PC
-   **I²C**: Updates OLED display with difficulty, questions, and
    results

### GUI Side (Python 3)

-   **PyQt5** → GUI framework
-   **PySerial** → Serial communication with STM32
-   **Qt Material** → Modern theme for GUI

GUI Features: - Request new questions (`Yeni Soru`)
- Enter and send answers
- View results (`Sonucu Gör`)

------------------------------------------------------------------------

## 📂 Project Structure
    |── Core
          |── src
               ├── main.c   # STM32 firmware (embedded side)
    ├── main_pyqt.py        # Python GUI application

------------------------------------------------------------------------

## ⚙️ Installation & Usage

### 1. Embedded Side

1.  Open `main.c` in **STM32CubeIDE**
2.  Flash firmware onto **STM32F411E-DISCO**
3.  Connect:
    -   USB cable (UART)
    -   OLED display (I²C)
    -   Potentiometer (ADC input)

### 2. Python GUI

1.  Install dependencies:

    ``` bash
    pip install pyqt5 pyserial qt-material
    ```

2.  Connect STM32 board via USB (check port, e.g., `COM5` on Windows).

3.  Run the GUI:

    ``` bash
    python main_pyqt.py
    ```

------------------------------------------------------------------------

## 🎮 How It Works

1.  User selects difficulty with potentiometer
2.  GUI button **Yeni Soru** requests a new question
3.  Question is displayed on GUI and OLED
4.  User submits an answer in the GUI
5.  STM32 checks the answer and shows feedback via LEDs + OLED
6.  GUI button **Sonucu Gör** displays total performance stats

------------------------------------------------------------------------
### Notes
- The STM32 communicates with the PC over **USB CDC (Virtual COM Port)**.  
- Serial communication can be tested using **Hercules Setup Utility** before running the Python GUI.
------------------------------------------------------------------------
