import sys
import urllib.request

class USVisaAppointmentChecker:
  def __init__(self, city_code_file="us_embassy_city_code"):
    self.us_appointment_url = "https://travel.state.gov/content/travel/resources/database/database.getVisaWaitTimes.html?aid=VisaWaitTimesHomePage&cid="
    self.city_map = {}
    self.visa_type = ["Visitor Visa", "Student/Exchange Visitor Visa", "All Other Nonimmigrant Visa"]
    with open(city_code_file) as file:
      for line in file:
        line = line.strip()
        # Ignore comment lines
        if line.startswith("#"):
          continue
        code_val_map = eval(line)
        self.city_map[code_val_map["value"]] = code_val_map["code"]

  def get_city_code(self, city):
    if (city in self.city_map):
      return (self.city_map[city])
    else:
      raise RuntimeError( "City not found! Check/update availiable cities." +
                          "\nHere are availiable cities:\n" + " ,".join(self.city_map.keys()) )

  def check_appointment_times(self, city):
    city_code = self.get_city_code(city.strip())
    response = urllib.request.urlopen(self.us_appointment_url+city_code)
    appointment_type = response.read().decode("utf-8").strip().split(",")
    return dict(zip(self.visa_type, appointment_type))

def main():
  if (len(sys.argv) != 2):
    print("Usage: \n\tpython3 USVisaAppointmentChecker.py [us embassy city]")
    sys.exit(1)
  visa_appt = USVisaAppointmentChecker()
  appt_times = visa_appt.check_appointment_times(sys.argv[1])
  for i in appt_times:
    print (i + " --- " + appt_times[i])

if __name__ == '__main__':
  main()

