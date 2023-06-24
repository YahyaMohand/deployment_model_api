from datetime import datetime

import score_prefect
from dateutil.relativedelta import relativedelta
from prefect import flow


@flow
def ride_duration_prediction_backfill():

    start_date = datetime(year=2021, month=3, day=1)
    end_date = datetime(year=2022, month=4, day=1)

    d = start_date

    while d <= end_date:

        score_prefect.ride_duration_prediction(
            run_id='0b2rf6a1ef3c4e6280d5ajfdb94c68ul',
            taxi_type='green',
            run_date=d
        )

        d = d + relativedelta(months=1)


if __name__ == '__main__':
    ride_duration_prediction_backfill()