# Rain Gauge Plugin

This plugin works with the [Hydreon RG-15 rain gauge](https://store.hydreon.com/RG-15.html). It will periodically sample and publish the Acc, EventAcc, TotalAcc, and RInt values.

Note: This plugin requires access to the rain gauge's serial port.

## Debugging Steps

This plugin is challenging to debug and test as it uses a serial device which is not easily simulated and can only have 1 "writer"/"reader" at a time. The following steps can be performed to test code changes on real hardware.

1) Kill any running k3s pods of the raingauge plugin

```
for s in $(kubectl get deployment | awk '/plugin-raingauge/ {print $1}'); do
    kubectl delete "deployment/$s"
done
```

2) Login to the RPi and install docker.io.

```
mkdir /media/plugin-data/docker
ln -s /media/plugin-data/docker/
apt-get update
apt-get install docker.io
```

3) Clone code to the RPi
4) Edit the `main.py` file and comment out the `plugin` publish stuff
5) Edit the `Dokerfile` to add `"--device", "/dev/ttyUSB0", "--debug"` to the `ENTRYPOINT`
5) Build your docker container

```
docker build -t testrain .
```

6) Run it and debug / test

```
docker run -it --rm --privileged testrain:latest
```

7) Clean-up docker on the RPi

```
service docker stop
rm -rf /media/plugin-data/docker
```

8) Reboot the RPi to wipe the cloned code and other files in the tmpfs
