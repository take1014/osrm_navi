# install dependencies
sudo apt update
# install docker
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
sudo systemctl start docker
sudo systemctl enable docker
sudo docker --version
sudo usermod -aG docker $USER

# install qemu
sudo apt update
sudo apt install qemu-user-static binfmt-support 
sudo docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
sudo apt install -y  build-essential git cmake pkg-config doxygen libboost-all-dev libtbb-dev lua5.2 liblua5.2-dev libluabind-dev libstxxl-dev libstxxl1v5 libxml2 libxml2-dev libosmpbf-dev libbz2-dev libzip-dev libprotobuf-dev

# clone osrm-backend
git clone https://github.com/Project-OSRM/osrm-backend.git
cd ~/osrm-backend/docker
cp Dockerfile ../
cd ..
# build docker image
sudo docker buildx build --platform linux/arm64/v8 --tag osrm-backend-arm64:latest .
# save docker image
sudo docker save -o osrm-backend-arm64.tar osrm-backend-arm64

# add swapfile
sudo fallocate -l 12G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo "/swapfile none swap sw 0 0" | sudo tee -a /etc/fstab
sudo swapon --all
sudo swapon --show

# download osm pbf
cd ~/
mkdir japan
cd japan
wget http://download.geofabrik.de/asia/japan-latest.osm.pbf

# extract
sudo docker run -t -v "${PWD}:/data" osrm-backend-arm64 osrm-extract -p /opt/car.lua /data/japan-latest.osm.pbf
sudo docker run -t -v "${PWD}:/data" osrm-backend-arm64 osrm-partition  /data/japan-latest.osrm
sudo docker run -t -v "${PWD}:/data" osrm-backend-arm64 osrm-customize  /data/japan-latest.osrm
