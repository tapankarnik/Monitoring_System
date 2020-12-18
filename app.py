import pprint
import docker
from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

jobs = {}

@app.route('/job_status', methods=['GET'])
def jobs_status():
    return jobs, 200

@app.route('/job_done', methods=['POST'])
def job_completion():

    if request.is_json:
        data = request.get_json()
        try:
            if len(data['job_name'])>20 or len(data['job_name'])==0 or data['job_name'] == None:
                raise Exception('Invalid Job Name')
            if data['num_jobs']<0 or data['num_jobs']==0 or data['num_jobs']>100:
                raise Exception('Invalid Number of Jobs')
            if data['job_id']<0 or data['job_id']>=data['num_jobs']:
                raise Exception('Invalid Job ID')
            if data['job_duration']<=0 or data['job_duration']>30:
                raise Exception('Invalid Job Duration')

        except Exception as e:
            return "Invalid Input" + str(e), 400

        job_name = data['job_name']
        num_jobs = data['num_jobs']
        job_duration = data['job_duration']
        
        if job_name in jobs:
            if jobs[job_name]["total"] == jobs[job_name]["completed"]:
                return "Don't send more jobs.", 400
            else:
                jobs[job_name]["completed"] += 1
        else:
            jobs[job_name] = {
                    "completed": 1,
                    "total": num_jobs,
            }

        return b"OK", 200

    else:
        return b"Not a JSON input", 400

@app.route('/status', methods=['GET'])
def status_update():

    client = docker.from_env()
    containers = client.containers.list()
    container_list = [container.name for container in containers]
    status_list = []
    for container in containers:
        stats = container.stats(stream=False)
        try:
            cpu_stats = round(stats['cpu_stats']['cpu_usage']['total_usage'] / (800000000*8), 3),
        except Exception:
            cpu_stats = None

        try:
            mem_stats = round(stats['memory_stats']['usage'] / stats['memory_stats']['limit'],3)
        except Exception:
            mem_stats = None
        
        print(type(cpu_stats))
        cpu_mem_stats = {
                'cpu_percentage': cpu_stats[0],
                'mem_percentage': mem_stats
                }
        name_and_stats = {
                'name': container.name,
                'stats': cpu_mem_stats
                }
        status_list.append(name_and_stats)
        print(cpu_mem_stats)
    return jsonify(status_list), 200


if __name__ == "__main__":
    print("Starting Monitoring Subsystem")
    app.run(host='0.0.0.0', port=5031, debug=True)
