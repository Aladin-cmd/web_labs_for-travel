import poststr as post
from send import send_email,gmail_password,gmail_user

persons=["prohord576@gmail.com","testaccmail1d@gmail.com"]
def load_test_email():
    ut=post.M2MPostRequestUtility()
    sttres= post.StressTest(ut)
    data=sttres.send_parallel_requests(3)
    message=f"\nNumber of request:{data[0]} ms \n"\
            f"All requeusts finish time:{data[1]} ms \n" \
            f"Median response time:{data[2]} ms \n" \
            f"Average response time:{data[3]} ms \n" \
            f"Max response time:{data[4]} ms \n" \
            f"Min response time:{data[5]} ms "
    send_email(persons,"Stress test",message,gmail_user,gmail_password)


if __name__=="__main__":
    load_test_email()
