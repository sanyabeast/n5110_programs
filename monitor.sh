#!bin/sh
# monitor.sh 
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
echo $DIR
sudo python "$DIR/py/monitor.py"
