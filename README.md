# Internet test speed recorder

This repo made for testing speed on download, upload and ping and record the result in log file with csv format.

## Usage
We have tow script here to do the work:
- scan.py
- getData.py

The scripts provids a help menu by runing the command followed with -h argument
```powershell
python3 scan.py -h
```
and
```powershell
python3 getData.py -h
```

### scan.py:
This script make the scan and return data as followe
```json
{"Date": "01-02-2022 11:37:13", "Download": 94376540.371672286, "Upload": 1065561.1454864491, "Ping": 61.744}
```
Speed data recorded for download and upload are bytes 'B' values

### getDate.py
After collecting your recored, it's time to get and export your data to excel table filtred by your choice.

#### Testing

> - command

```poweshell
python3 getData.py -f D 
```

> - log.csv

 ```csv
01-02-2022 11:37:13,94376540.371672286,2065561.1454864491,61.744
01-02-2022 11:37:13,64376540.371672286,5065561.1454864491,22.744
02-02-2022 11:37:13,34376540.371672286,2065561.1454864491,21.744
02-02-2022 11:37:13,94376540.371672286,1065561.1454864491,31.744
02-02-2022 11:37:13,44376540.371672286,6065561.1454864491,63.744
```
> - Table

| Date                | Download | Upload | Ping  |
|---------------------|----------|--------|-------|
| 01-02-2022 11:37:13 | 79.38    | 3.57   | 61.71 |
| 02-02-2022 11:37:13 | 62.56 | 8.23 | 82.11 |
