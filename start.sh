#!/bin/bash

echo "Starting all project services..."

echo "-> Starting Task 1 on port 8501..."
(cd Task1 && streamlit run main.py --server.port 8501) &


echo "-> Starting Task 2 on port 8000..."
(cd Task2 && streamlit run main.py --server.port 8000) &

echo "----------------------------------------"
echo "All services are starting up."
echo "Task 1 will be available at http://localhost:8501"
echo "Task 2 will be available at http://localhost:8000"
echo "Press Ctrl+C in this terminal to stop all services."

wait