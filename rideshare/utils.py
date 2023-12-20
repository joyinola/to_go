import os
import requests
import datetime

from .models import AccountDetail, Rider, User

headers = {"Authorization": f"Bearer {os.getenv('paystack_secret')}"}


def initialize_trans(data):
    """
    initializes transactions i.e passenger to togo
    receives email and amount
    sends auth url and reference
    """

    url = "https://api.paystack.co/transaction/initialize"

    data = {"email": data.get("email"), "amount": data.get("amount")}

    response = requests.post(url, data=data, headers=headers)

    return response.json()


def make_transfer(data):
    """
    transfer money to rider
    """
    url = "https://api.paystack.co/transfer"
    data = {
        "source": "balance",
        "amount": data.get("amount"),
        "recipient": data.get("recipient"),
        "reference": data.get("reference"),
    }
    response = requests.post(url, data = data, headers=headers)
    print(response.json())
    return response.json()


# def finalize_transfer(data):
#     url = "https://api.paystack.co/finalize_transfer"
#     data = {
#         "transfer_code": data.get("tranfer_code"),
#         "amount": data.get("amount"),
#         "recipient": data.get("recipient"),
#     }
#     response = requests.post(url, headers=headers)

#     return response.json()


def verify_account_no(data):
    url = "https://api.paystack.co/bank/resolve"

    params = {
        "account_number": data.get("account_number"),
        "bank_code": data.get("bank_code"),
    }
    response = requests.get(url, headers=headers, params=params)

    return response.json()


def create_recipient(data):
    url = "https://api.paystack.co/transferrecipient"

    data = {
        "account_number": data.get("account_number"),
        "bank_code": data.get("bank_code"),
        "name": data.get("account_name"),
        "currency": "NGN",
        "type": "nuban",
    }

    response2 = requests.post(url, headers=headers, data=data)

    return response2.json()


def riders_working_today(
    riders_list, current_day
):  # returns list of riders scheduled to work that day
    riders_working_day = [
        rider_ for rider_ in riders_list if current_day in rider_.schedule.get("days")
    ]
    return riders_working_day


def riders_working_now(
    riders_list, current_time: datetime
):  # returns list of riders who are working at the "time"
    riders_working_now_list = []
    for riders in riders_list:
        start_time = riders.schedule.get("start_time").split(":")
        end_time = riders.schedule.get("end_time").split(":")
        current_time_ = str(current_time).split(":")

        start_time_hr = int(start_time[0][:2])
        start_time_min = int(start_time[1][:2])

        end_time_hr = int(end_time[0][:2])
        end_time_min = int(end_time[1][:2])

        # converts from 12hr clock to 24 hr clock

        # 12pm in 12hr clock is 12pm in 24hrclock
        if end_time[1][2:] == " PM" and not (end_time_hr == 12):
            end_time_hr += 12

        # if 12AM set 24 clock to 00
        elif end_time[1][2:] == " AM" and (end_time_hr == 12):
            end_time_hr -= 12

        # 12pm in 12hr clock is 12pm in 24hrclock
        if start_time[1][2:] == " PM" and not (end_time_hr == 12):
            start_time_hr += 12

        # if 12AM set 24 clock to 00
        elif start_time[1][2:] == " AM" and (start_time_hr == 12):
            start_time_hr -= 12

        start_time_obj = datetime.time(
            start_time_hr, start_time_min
        )  # start time is a string i.e 08:10 AM --this creates a datetime object from it
        end_time_obj = datetime.time(end_time_hr, end_time_min)
        current_time_obj = datetime.time(
            int(current_time_[0][:2]), int(current_time_[1][:2])
        )

        if start_time_obj <= current_time_obj <= end_time_obj:
            riders_working_now_list.append(riders)

    return riders_working_now_list
