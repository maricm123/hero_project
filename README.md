# This repository contains the codebase for job application (Mini project/task).

# Project Hero

## Table of Contents

- [Introduction](#introduction)
- [Requirements](#requirements)
- [Installation](#installation)

## Requirements

- Docker (Ensure Docker is installed and running on your system)

## Installation

- Clone repository
https://github.com/maricm123/hero_project
- cd hero_project
- cd hero (there is docker-compose file)
- run 'docker compose up --build' command to build containers for app (Python, PostgreSql)
- Maybe you will need to stop postgres service on your machine (because of ports)
- If you use Windows, you can do that in Services, find postgresql Server, right click on it and stop,
  then re-run docker 'compose up --build' command again.

If successful started:
- open http://localhost:8000/api_device/device-config/ for DRF playground, to test device config with json data
- open http://localhost:8000/api_frontend/frontend-config/ for DRF playground, to test frontend config with json data

You can find JSON data that I used to test in json.txt file in root folder
