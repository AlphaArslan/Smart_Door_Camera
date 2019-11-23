echo "Waiting for 10 seconds"
sleep 10
cd /home/pi/Desktop/Alpha/Smart_Door_Camera
echo "Running media.py"
python3 media.py &
echo "Running main.py"
python3 main.py &
echo "Running server.py"
cd webpage
python3 server.py &
