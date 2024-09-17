#!/bin/bash
RABBITMQ_IP=$(getent hosts rabbitmq | awk '{ print $1 }')
echo "RabbitMQ IP: $RABBITMQ_IP"
echo "RABBITMQ_HOST=$RABBITMQ_IP" >>/app/.env
echo "RABBITMQ_PORT=5672" >>/app/.env
python -m "product_production.main"
