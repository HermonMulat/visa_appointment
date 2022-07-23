import os, sys
from twilio.rest import Client

class TextMessageSender:
  def __init__(self, account_sid = os.environ['TWILIO_ACCOUNT_SID'],
                auth_token=os.environ['TWILIO_AUTH_TOKEN'],
                send_from = os.environ['TWILIO_PHONE_NUMBER']):
    self.client = Client(account_sid, auth_token)
    self.send_from = send_from

  def send_text_to(self, text_body, send_to):
    print("Sending text message to [" + send_to + "]...")
    message = self.client.messages.create(body=text_body,
                  from_=self.send_from, to=send_to)
    print("Sent!")
    return message

def main():
  if (len(sys.argv) != 3):
    print("Usage: \n\tpython3 TextMessageSender.py [text message body] [send_to]")
    sys.exit(1)
  txt = TextMessageSender()
  txt.send_text_to(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
  main()
