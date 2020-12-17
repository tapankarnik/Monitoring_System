# Monitoring Subsystem for Data Center Network

Part of the Chaos Testing Suite

[Data Center Network](https://github.com/tapankarnik/DCN)

[Stress Testing Subsystem](https://github.com/tapankarnik/Stress-Testing)

[Chaos Testing Subsystem](https://github.com/tapankarnik/Chaos-Testing)

This subsystem exposes a webhook for the jobs from the DCN to report their completion and provides metrics to the GUI.

Jobs are reported by the DCN workers at localhost:5031/job_done.

The GUI may request the job status at localhost:5031/job_status

The GUI may request the DCN information at localhost:5031/status

Sample JSON for reporting completion of jobs

    {
        "job_name":"Solar",
        "job_id":1,
        "num_jobs":8,
        "job_duration":4
    }


