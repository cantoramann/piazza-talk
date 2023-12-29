# See README.md to set up environment variables

import os
authority = os.environ.get('accept')
print(authority)

cookies = {
    'session_id': os.environ.get('session_id'),
    'last_piaz_user':  os.environ.get('last_piaz_user'),
    'AWSALB':  os.environ.get('AWSALB'),
    'AWSALBCORS': os.environ.get('AWSALBCORS'),
    'piazza_session': os.environ.get('piazza_session'),
}

headers = {
    'authority': os.environ.get('authority'),
    'accept':  os.environ.get('accept'),
    'accept-language':  os.environ.get('accept_language'),
    'content-type':  os.environ.get('content_type'),
    'csrf-token':  os.environ.get('csrf_token'),
    'origin': os.environ.get('origin'),
    'sec-ch-ua': os.environ.get('sec_ch_ua'),
    'sec-ch-ua-mobile': os.environ.get('sec_ch_ua_mobile'),
    'sec-ch-ua-platform': os.environ.get('sec_ch_ua_platform'),
    'sec-fetch-dest': os.environ.get('sec_fetch_dest'),
    'sec-fetch-mode': os.environ.get('sec_fetch_mode'),
    'sec-fetch-site': os.environ.get('sec_fetch_site'),
    'user-agent': os.environ.get('user_agent'),
}

REFERER_BASE=os.environ.get('referer_base') # 'https://piazza.com/class/...?cid='
STUDENT_NID=os.environ.get('nid')