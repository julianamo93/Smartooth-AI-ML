#!/bin/bash

# Iniciar o servidor Flask em background
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 run:app &

# Manter o container rodando
wait