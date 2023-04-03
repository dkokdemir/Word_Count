# With this script, you can simply run it using the command 
#"bash script.sh" 
#in the terminal to create and activate the virtual environment, 
#install packages, and run the app. 

#Note that this assumes the requirements.txt and app.py files 
#are in the same directory as the script.

#!/bin/bash

# Create a virtual environment
python3 -m venv myenv

# Activate the virtual environment
source myenv/bin/activate

# Install packages from requirements.txt
pip install -r requirements.txt

# Run app.py
python app.py

# Deactivate the virtual environment
deactivate

# dkokdemir | 03 April 2023 | V.10
