#!/bin/env python3

import speedtest, subprocess, os, time, argparse, sys
from datetime import datetime
from colorama import Fore, Style

#------------------------------------------------------------------------------------------------------
# Setup arguments
parser = argparse.ArgumentParser(description="Network speed recorder osing ookla api cli speedtest, keep in mind that one test may take more than one minute")
parser.add_argument("-w", "--wait", type=int, help='waiting time bitween scans', required=True)
parser.add_argument("-t", "--time", help='hours to shutdown the script ex: -t 5, 5 hours', required=True)
parser.add_argument("-o", "--output", action="store_true", default="./log.csv", help="path to output")
parser.add_argument("-v", "--verbose", action="store_true", help="print speedtest values")
parser.add_argument("-q", "--quit", action="store_true", help="print only psswords")

args = parser.parse_args()

#------------------------------------------------------------------------------------------------------
# Check if non args montioned to print help menu
if len(sys.argv) < 2:
    parser.print_help()
    sys.exit()

#------------------------------------------------------------------------------------------------------
# Check connection with internet
platform = sys.platform
match platform:
    case "linux":
        cnx = subprocess.call(["ping", "-c", "2", "8.8.8.8"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, timeout=5)
    case "win32":
        cnx = subprocess.call(["ping", "-n", "2", "8.8.8.8"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, timeout=5)
if cnx != 0:
    print(f"{Fore.RED}No internet connection !!{Style.RESET_ALL}")
    sys.exit()

#------------------------------------------------------------------------------------------------------
def test():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        st.download()
        st.upload()
        res = st.results
    except:
        st = speedtest.Speedtest()
        res = st.results
    while 1:
        if res.download != 0 and res.upload != 0:
            return {"Download": res.download, "Upload": res.upload, "Ping": res.ping}
    

#------------------------------------------------------------------------------------------------------
def record(data):
    # Record data to file log.csv
    with open(args.output, "a+") as log:
        log.write(f"{data['Date']},{data['Download']},{data['Upload']},{data['Ping']}\n")

#------------------------------------------------------------------------------------------------------
# Convert from bytes to megabytes
def convert_size(speed):
    return round(speed / pow(1024, 2), 2)
#------------------------------------------------------------------------------------------------------
def main():
    finalTime = time.time() + (float(args.time) * 3600)
    while 1:
        if time.time() < finalTime:
            info = test()
            date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            info["Date"] = date
            if info["Download"] != 0 and info["Upload"] != 0 and info["Ping"] != 0:
                record(info)
                if args.verbose:
                    print(f'Date: {info["Date"]},  Download: {Fore.GREEN}{convert_size(info["Download"])}{Style.RESET_ALL}, Upload: {Fore.BLUE}{convert_size(info["Upload"])}{Style.RESET_ALL}, Ping: {info["Ping"]}')
            time.sleep(args.wait)
            continue
        else:
            break
    sys.exit()

#------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()

#------------------------------------------------------------------------------------------------------