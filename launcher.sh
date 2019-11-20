echo "Waiting for 60 seconds"
sleep 60
cd /home/pi/Desktop/alpha/Smart_Door_Camera
echo "Running media.py"
python3 media.py > log/media_log.txt &
echo "Running main.py"
python3 main.py > log/main_log.txt &
echo "Running server.py"
cd webpage
python3 server.py > log/server_log.txt &
