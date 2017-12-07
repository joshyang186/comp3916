#!/bin/bash

echo "list tasks"
echo "--------------------------------------------------------------------------"
curl -i -H "Content-Type: application/json" -u josh:COMP3916 -X GET http://localhost:5000/tasks

echo "get one task"
echo "--------------------------------------------------------------------------"
curl -i -H "Content-Type: application/json" -u josh:COMP3916 -X GET http://localhost:5000/tasks/1

echo "post one task"
echo "--------------------------------------------------------------------------"
curl -i -H "Content-Type: application/json" -u josh:COMP3916 -X POST -d '{"start_date": "12/5/2017 10:00", "end_date": "12/5/2017 15:00", "priority": "low", "description": "insert the data", "status": false}' http://localhost:5000/tasks

echo "put one task"
echo "--------------------------------------------------------------------------"
curl -i -H "Content-Type: application/json" -u josh:COMP3916 -X PUT -d '{"status": true}' http://localhost:5000/tasks/1

echo "delete one task"
echo "--------------------------------------------------------------------------"
curl -i -H "Content-Type: application/json" -u josh:COMP3916 -X DELETE http://localhost:5000/tasks/1

echo "testing completed."
