import os
import requests

headers = {
         'Authorization': f"Bearer {os.getenv('paystack_secret')}"
     }

def initialize_trans(data):
     """
    receives email and amount
    sends auth url and reference
     """

     url = 'https://api.paystack.co/transaction/initialize'


     data = { 
         "email": data.get('email'),
         "amount": data.get('amount')
    #  'callback_url': 'localhost:8000/verify_pay/'

     }

     response = requests.post(
         url,
         data = data,
         headers = headers
     )
     return response.json()
  
def send():
    """
    create transfer recipient
    generate tfr reference
    initiate a trans - if sucess returns status -pending else error, if error retry with the same reference
    """

def verify(reference):
     
    #  print(reference)
     """
     receives reference created at initialize
     returns data.status success
     """
     url = f"https://api.paystack.co/transaction/verify/{reference}"
    

     response = requests.get(
         url,
         headers = headers
     )

     return response.json()


def list_banks(data):
     url = f"https://api.paystack.co/bank/"
     params = {
         "country":"nigeria"
     }
     response = requests.get(
         url,
         headers = headers
     )

     return response.json()

def verify_account_detail(data):
     url = f"https://api.paystack.co/bank/resolve/"

     params = {
         "account_number":data.get('account_no'),
          "bank_code":data.get('bank_code')
     }
     response = requests.get(
         url,
         headers = headers
     )

     return response.json()

def transfer_recipient(data):
    """send account get rcipient code"""
    url = "https://api.paystack.co/transferrecipient"
    data = {
          "type":"nuban",
          "name":data.get('name'),
          "account_number":data.get('account_number'),
          "bank_code":data.get('bank_code'),
     }
    response = requests.post(
         url,
         headers = headers
     )

    return response.json()

def make_transfer(data):
    url = "https://api.paystack.co/transfer"
    data = {
          "source":"balance",
          "amount": data.get('amount'),
          "recipient":data.get('recipient')
     }
    response = requests.post(
         url,
         headers = headers
     )

    return response.json()

def finalize_transfer(data):
    url = "https://api.paystack.co/finalize_transfer"
    data = {
          "transfer_code":data.get('tranfer_code'),
          "amount": data.get('amount'),
          "recipient":data.get('recipient')
     }
    response = requests.post(
         url,
         headers = headers
     )

    return response.json()
