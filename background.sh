#!/bin/bash
cd /home/pi/Desktop/piano-visualizer/
source .env/bin/activate
sudo nohup python3 src/visualizer.py run &
cd recordings/
sudo nohup python3 -m http.server 80 &