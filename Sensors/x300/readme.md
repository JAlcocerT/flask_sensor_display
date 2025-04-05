> [x300](https://jalcocert.github.io/JAlcocerT/asrock-x300-home-server/)


```sh
sudo apt update
sudo apt install lm-sensors

sudo sensors-detect
```

```sh
sudo modprobe nct6775
sensors
#sensors > sensor_output.txt
```

If we run some [benchmarks](https://jalcocert.github.io/JAlcocerT/benchmarking-computers/), you can see how these CPU Temps, fan speeds...change:

```sh
sysbench --test=cpu --cpu-max-prime=20000 --num-threads=4 run #4 cores
#See the variables quickly
sensors | grep "Tctl"
sensors | grep -E "Tctl|fan2|PPT"
```

See the data from the x300:
```sh
python3 data.py
```

Save it into a DB:

```sh
python3 ./Sensors/x300/sensor_loger.py
```

See whats loaded:

```sh
sudo apt install sqlite3
sqlite3 --version

sqlite3 ./sensor_data.db

#SELECT name FROM sqlite_master WHERE type='table';
#.tables
#.schema sensor_data

SELECT * FROM sensor_data;
SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 5;
#.quit #when you are done!
```