from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule
from score_prefect import ride_duration_prediction

deployment = Deployment.build_from_flow(
    flow=ride_duration_prediction,
    name='ride_duration_predict',
    version=2,
    work_queue_name='ml',
    work_pool_name='zoompool',
    parameters={
        "taxi_type": 'green',
        "run_id": '0b2rf6a1ef3c4e6280d5ajfdb94c68ul',
    },
    schedule=CronSchedule(cron="0 3 2 * *"),
)

if __name__ == "__main__":
    deployment.apply()