from sendemail import send_email, gmail_password, gmail_user
from main import m2m_request, m2m_request_get, m2m_request_post
import requests
#api client
# result = m2m_request("AKIAZJIYWTQ64XZGHXER", "oRlL+Ms+hs6GRRN+/CQ+MpJgM40cr5uuwVli95u0", 30.74716231727497,
#                 -95.61527307112493)
#
# get=m2m_request_get("AKIA2TITFGWE5F7HF5PB", "p60sVYmX1SBwUkKfGZF9N5Aml9plS4Izl07Bl1v9",
#                                45.6696163800542, -122.5038830583887)
#
# post=m2m_request_post("AKIA2TITFGWE5F7HF5PB", "p60sVYmX1SBwUkKfGZF9N5Aml9plS4Izl07Bl1v9")
#
#
# status1= result.status_code
# time1= result.elapsed.total_seconds()
# status2= get.status_code
# time2= get.elapsed.total_seconds()
# status3= post.status_code
# time3= post.elapsed.total_seconds()
#
# verify=[[time1,status1],[time2,status2],[time3,status3]]
# def check(time_result, response_code):
#     if time_result > 0.5 or response_code != 200:
#         message = "Following results: time-{} ,status-{}".format(time_result, response_code)
#         send_email("testaccmail1d@gmail.com", "Test send", message, gmail_user, gmail_password)
#     else:
#         print("Everything is fine")
# for v in verify:
#     check(v[0],v[1])


#Person that will get email
persons=["prohord576@gmail.com","testaccmail1d@gmail.com"]

#Verify if response time is less than 0.5 and response is successfull
def check_api(req):
    result=req
    time=result.elapsed.total_seconds()
    status=result.status_code
    if time > 0.5 or status != 200:
        try_again=req
        new_time=try_again.elapsed.total_seconds()
        new_status=try_again.status_code
        print(req.text)
        if new_time>0.5 or new_status!=200:
            message = "Following results:\n" \
                      "Time\n" \
                      "Expected: 0.5; Actual:{}\n" \
                      "Status Code\n" \
                      "Expected 200; Actual:{}.\n" \
                      "Response:{}".format(new_time, new_status,try_again.text)
            send_email(persons, "API", message, gmail_user, gmail_password)
            print(try_again.text)
        else:
            print("OK")
    else:
        print("OK")

reques=[
    m2m_request("AKIAZJIYWTQ64XZGHXER", "oRlL+Ms+hs6GRRN+/CQ+MpJgM40cr5uuwVli95u0", 30.74716231727497,-95.61527307112493),
    m2m_request_get("AKIA2TITFGWE5F7HF5PB", "p60sVYmX1SBwUkKfGZF9N5Aml9plS4Izl07Bl1v9",
                               45.6696163800542, -122.5038830583887),
    m2m_request_post("AKIA2TITFGWE5F7HF5PB", "p60sVYmX1SBwUkKfGZF9N5Aml9plS4Izl07Bl1v9")
]

for _ in reques:
    check_api(_)