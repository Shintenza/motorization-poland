import requests
from time import sleep
from urllib.parse import urlparse, parse_qs
from csv import writer
import threading

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = (         # pyright: ignore
    "ALL:@SECLEVEL=1"  
)

region_codes_url = "https://api.cepik.gov.pl/slowniki/wojewodztwa"


res = requests.get(region_codes_url)
parsed_region_dict = res.json()

region_codes = {}

for element in parsed_region_dict["data"]["attributes"]["dostepne-rekordy-slownika"]:
    region_codes.update({element["klucz-slownika"]: element["wartosc-slownika"]})

cols = [
    "Region",
    "Brand",
    "Model",
    "Source",
    "VehicleId",
    "CubicCapacity",
    "Weight",
    "FuelType",
    "Year",
    "ProductionYear",
    "DeregisterDate",
    "DeregisterReason",
    "AlternativeFuel",
]
del region_codes["XX"]

out_csv = open('./../data/registered_cars_complete.csv', 'w', encoding='utf-8')
writer_object = writer(out_csv)
writer_object.writerow(cols)

threads = []

lock = threading.Lock()

def get_data_for_year(year):
    thread_name = threading.current_thread().name
    for region_code in region_codes:
        data_url = f"https://api.cepik.gov.pl/pojazdy?wojewodztwo={region_code}&data-od={year}0101&data-do={year}1231&limit=500&filter[rodzaj-pojazdu]=SAMOCHÓD%20OSOBOWY&pokaz-wszystkie-pola=true"
        total_number_of_pages_link = ""

        max_pages = ""
        while True:
            try: 
                total_number_of_pages_link = requests.get(data_url).json()["links"]["last"]
                parsed_link = urlparse(total_number_of_pages_link)
                link_params = parse_qs(parsed_link.query)

                max_pages = link_params["page"][0]
                if int(max_pages) > 2:
                    break;
                else:
                    print(f"Failed getting max number of pages {threading.current_thread().name} retrying in 10 seconds")
                    sleep(3)
            except:
                sleep(3) 

        i = 0
        while i < int(max_pages):
            print(f"getting data for region: {region_code} (page: {i+1}/{max_pages}) on thread: {thread_name}")
            paginated_data_url = data_url + f"&page={i+1}"
            try:
                parsed_data = requests.get(paginated_data_url).json()
                for element in parsed_data["data"]:
                    id = element["id"]
                    element = element["attributes"]
                    production_year = -1
                    if (element["sposob-produkcji"] is not None) and element["sposob-produkcji"].isdigit():
                        production_year = int(element["sposob-produkcji"])
                    if (element["rok-produkcji"] is not None) and element["rok-produkcji"].isdigit():
                        production_year = int(element["rok-produkcji"])
                    new_row = [
                        region_codes[region_code],
                        element["marka"],
                        element["model"],
                        element["pochodzenie-pojazdu"],
                        id,
                        element["pojemnosc-skokowa-silnika"],
                        element["masa-wlasna"],
                        element["rodzaj-paliwa"],
                        year,
                        production_year,
                        element["data-wyrejestrowania-pojazdu"],
                        element["przyczyna-wyrejestrowania-pojazdu"],
                        element["rodzaj-pierwszego-paliwa-alternatywnego"],
                    ]
                    lock.acquire()
                    writer_object.writerow(new_row) 
                    lock.release()
                i+=1
            except Exception as e:
                print(f"program crashed: page {i + 1}, region: {region_code}, thread: {thread_name}! Error: {e}")
                sleep(10)


for i in range(2010, 2022+1):
    thread = threading.Thread(target=get_data_for_year, args=(i,), name=f"year_{i}")
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

out_csv.close()
