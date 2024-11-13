# cesit_dijitallesme

# Install

## Raspbian OS

## Python

### 1. Clone the Repository
Start by cloning this GitHub repository to your local machine:
```bash
git clone https://github.com/username/repository-name.git
cd repository-name
```

### 2. Create a Virtual Environment
It's best to use a virtual environment to manage dependencies and avoid conflicts.

#### Using `venv` (comes with Python)
Run the following command to create a virtual environment in the project folder:
```bash
python3 -m venv env
```

#### Using `virtualenv` (if preferred)
If you prefer `virtualenv`, first install it (if you haven't already):
```bash
pip install virtualenv
```
Then create a virtual environment:
```bash
virtualenv env
```

### 3. Activate the Virtual Environment
Activate the virtual environment depending on your operating system:

- **On Windows**:
  ```bash
  .\env\Scripts\activate
  ```
- **On macOS/Linux**:
  ```bash
  source env/bin/activate
  ```

Once activated, your command line should show the environment name (`env`) at the start of the prompt, indicating you're now using the isolated Python environment.

### 4. Install Dependencies
Install all required Python packages using `pip`:
```bash
pip install -r requirements.txt
```

Make sure the `requirements.txt` file is up-to-date with all the necessary packages. If not, you can generate one using:
```bash
pip freeze > requirements.txt
```

## Usage
After setting up the environment and installing dependencies, you're ready to run the project.

### Running the Project
Run the main script as follows:
```bash
python main.py
```

Replace `main.py` with the appropriate entry point for your project.

## Deactivating the Virtual Environment
To exit the virtual environment when you're done, simply type:
```bash
deactivate
```

## Additional Information
- **Updating Dependencies**: If you need to add new packages, install them with `pip install package_name`, and update the `requirements.txt` file with `pip freeze > requirements.txt`.
- **Troubleshooting**: If

## App Service
```
sudo cp conf/cesit_core.service /etc/systemd/system/
sudo systemclt enable cesit_core.service
sudo systemclt start cesit_core.service
```

## VPN
Copy and give vpn-login information with ```nano```.
```
sudo cp myconnection.conf /etc/vpnc/
sudo nano /etc/vpnc/myconnection.conf

sudo cp conf/vpnc@.service /lib/systemd/system/vpnc@.service
sudo systemclt enable vpnc@myconnection.service
sudo systemclt start vpnc@myconnection.service
```

# Requirements
- ```pip3 install pymongo RPLCD smbus2 ```
- ```pip3 install "paho-mqtt<2.0.0"```

# Hardware

## Pinout
![pinout](img/raspberry_zero_pinout.png)
imgref: indibit.de
## Input Circuit
![input_circuit](img/input_circuit.png)

# Remarks
- An external pull-up sensor is being used.
If an internal pull-up must be used, the entry `pull_up_down=GPIO.PUD_OFF` in `button_switch.py` within the line `GPIO.setup(self.gpio_no, GPIO.IN, pull_up_down=GPIO.PUD_OFF)` needs to be removed.
- A hex inverter is used before the GPIO input, so the signals are inverted.
- Currently, a 1 microfarad capacitor is installed for debouncing, which is very large. Either remove it or replace it with a 0.1 microfarad capacitor.
