#!/usr/local/bin/python3

import sys,time,datetime,traceback
from TextMessageSender import TextMessageSender
from USVisaAppointmentChecker import USVisaAppointmentChecker

def main():
    appt_checker = USVisaAppointmentChecker()
    txt_sender = TextMessageSender()

    notify_wait_time_threshold,visa_type,city,send_to = get_inputs(appt_checker.visa_type)

    try:
        while True:
            appt_times = appt_checker.check_appointment_times(city)
            curr_wait_time = int(appt_times[visa_type].split()[0])
            text_body = "\n".join([ k + " -- " + v for k,v in appt_times.items()])
            # log current visa wait time
            now = "["+str(datetime.datetime.now())+"] "
            print("\n".join([ now + line for line in  text_body.split("\n")]))
            print("-"*80)
            if (curr_wait_time <= notify_wait_time_threshold):
              txt_sender.send_text_to(city + "\n" + text_body, send_to)
              break
            time.sleep(60) # sleep for a min
    except Exception:
        exception_msg = traceback.format_exc()
        txt_sender.send_text_to("Error:\n" + exception_msg, send_to)
        raise Exception
    print()

# get inputs from command line, with some input validation
def get_inputs(available_visa_types):
    if (len(sys.argv) != 5):
      print('Usage:\tpython3 notify_me.py [wait time threshold in days] "[visa type]" "[City]" "[Phone number to send text to]"' )
      print('\t./notify_me.py [wait time threshold in days] "[visa type]" "[City]" "[Phone number to send text to]"' )
      print('e.g:\tpython3 notify_me.py 7 "Visitor Visa" "Vancouver" "5551231234"')
      sys.exit(1)

    try:
      notify_wait_time_threshold = int(sys.argv[1])
    except ValueError:
      print ("Wait time threshold must be an integer")
      sys.exit(1)
    visa_type = sys.argv[2]
    if (visa_type not in available_visa_types):
      print ("Visa type must be one of [" + " , ".join(available_visa_types) + "]")
      sys.exit(1)
    city = sys.argv[3]
    send_to = sys.argv[4]
    print ("Input Values:")
    print("\tNotify Wait time threshold in days =", notify_wait_time_threshold)
    print("\tVisa Typw =", visa_type)
    print("\tCity =", city)
    print("\tPhone number to text for notification = ", send_to)
    print("-"*80)
    return (notify_wait_time_threshold,visa_type, city, send_to)


if __name__ == '__main__':
    main()

