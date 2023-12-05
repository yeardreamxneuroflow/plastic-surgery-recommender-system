#!/bin/bash

# sudo groupadd docker  # Already exists in Ubuntu 20.04
sudo usermod -aG docker $USER
newgrp docker

# Verify Installation
# TO-DO: Handle Sub-shell Issue
docker run hello-world
