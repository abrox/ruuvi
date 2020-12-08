# ruuvi
Gateway application to read data from ruuvi tag with rasperrypi. provide REST interface to read data to the logger device

sudo cp ruuvi-server.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ruuvi-server.service
sudo systemctl start ruuvi-server.service
