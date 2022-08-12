sid = 'student580'
token = 'edc82e540212f12b53c661755600bbc2d79d5a96'
url = 'http://13.127.181.8:8000/get-audio-demo'
#url='https://vocaroo.com/media_command.php?media=s1EOVpzKZQaw&command=download_wav'
from pprint import pprint
import requests


def connect_customer(sid, token,
                     customer_no, exotel_no, callerid, url,
                     timelimit=None, timeout=None,calltype="trans",
                     callback_url=None):
    return requests.post('https://twilix.exotel.in/v1/Accounts/{sid}/Calls/connect.json'.format(sid=sid),

auth =(sid, token),
data = {'From': customer_no,
        'To': exotel_no,
        'CallerId': callerid,
        'Url': url,
        'TimeLimit': timelimit,
        'TimeOut': timeout,
        'CallType': calltype,
        'StatusCallback': callback_url})


if __name__ == '__main__':
    r = connect_customer(
        sid, token,
        customer_no="+919162912126",
        exotel_no="08047103685",
        callerid="08047103685",
        url="http://my.exotel.in/exoml/start_voice/214054",
	#url="http://www.music.helsinki.fi/tmt/opetus/uusmedia/esim/a2002011001-e02-8kHz.wav",
        timelimit="15",  # This is optional
        timeout="15",  # This is also optional
        # calltype="trans",  # Can be "trans" for transactional and "promo" for promotional content
        # callback_url="<http//: your company URL>"  # This is also also optional
        )
    print(r.status_code)
    pprint(r.json())
