#!/bin/bash

SERVICE=$1

docker compose -f ./$SERVICE.yml up -d --build
