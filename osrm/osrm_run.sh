cd ~/japan
sudo docker run -t -i -p 5000:5000 -v "${PWD}:/data" osrm-backend-arm64 osrm-routed \
    --algorithm mld \
    --memory=4G \
    --threads=4 \
    /data/japan-latest.osrm
