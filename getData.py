#!/bin/env python3

import argparse, sys
from datetime import datetime
from colorama import Fore, Style
import pandas as pd

#------------------------------------------------------------------------------------------------------
# Setup arguments
parser = argparse.ArgumentParser(description="Read scan log.csv and gives you daily average in excel table.")
parser.add_argument("-f", "--filter", help='filter "H" for hours, "D" for days, "M" for months.', default="D", choices=["H", "D", "M"])
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("-q", "--quit", action="store_true")

args = parser.parse_args()

#------------------------------------------------------------------------------------------------------
# Check if non args montioned to print help menu
if len(sys.argv) <= 1:
    parser.print_help()
    sys.exit()

#------------------------------------------------------------------------------------------------------
# Convert from bytes to megabytes
def convert_size(speed):
    return round(speed / pow(1024, 2), 2)

#------------------------------------------------------------------------------------------------------
# Generate a name from given args
def sheetName(flag):
    match args.filter:
        case "D":
            name = "Daily_Averege"
        case "M":
            name = "Monthly_Average"
        case "Y":
            name = "Yearly_Averege"
    return name

#------------------------------------------------------------------------------------------------------
# Output informations
def echo(text):
    if not args.quit:
        print(text)

def info(text):
    if args.verbose:
        print(text)

#------------------------------------------------------------------------------------------------------
# Main function
def main(filter, name):
    # Get data from csv log and make a dataframe with spesified columns name
    echo(f"{Fore.YELLOW}[*]{Fore.CYAN} Get file log.csv and create dataframe..{Style.RESET_ALL}")
    df = pd.read_csv("log.csv", sep=",", names=["Date", "Download", "Upload", "Ping"])
    echo(f"{Fore.GREEN}[+]{Fore.BLUE} Dataframe created sucsessfuly.\n{Style.RESET_ALL}")
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y %H:%M:%S")
    info(f"{Fore.CYAN}[!]{Fore.MAGENTA} Number of rows: {Fore.YELLOW}{len(df)}{Style.RESET_ALL}") #-info
    info(f"{Fore.CYAN}[!]{Fore.MAGENTA} Date range of record: {Fore.YELLOW}{str(df.Date.values[0]).split('T')[0]} => {str(df.Date.values[-1]).split('T')[0]}{Style.RESET_ALL}\n") #-info

    # Convert values from bytes 'B' to megabytes 'MB'
    echo(f"{Fore.YELLOW}[*]{Fore.CYAN} Fetching data and create excel file..{Style.RESET_ALL}")
    df.Download = df.apply(lambda row: convert_size(row.Download), axis=1)
    df.Upload = df.apply(lambda row: convert_size(row.Upload), axis=1)

    # Groupby data by the day and calculate the averege of each day
    dff = df.set_index("Date").resample(filter).mean().round(2).dropna()

    # Export table to xlsx file
    dff.to_excel(name + "_Speed.xlsx", sheet_name=name)
    echo(f"{Fore.GREEN}[+]{Fore.BLUE} Datafram exported on '{name}_Speed.xlsx' filterd by '{filter}'{Style.RESET_ALL}")

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main(args.filter, sheetName(args.filter))
#------------------------------------------------------------------------------------------------------
echo(f"{Fore.GREEN}\n[+] Done.{Style.RESET_ALL}")
#------------------------------------------------------------------------------------------------------