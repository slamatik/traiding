from urllib.request import urlopen
from bs4 import BeautifulSoup
from time import time
import re
import pandas as pd

# todo finish parsing all data

data_nasdaq = pd.read_csv(r'C:\Users\slama\PycharmProjects\traiding\markets\nasdaq.csv')
data_nyse = pd.read_csv(r'C:\Users\slama\PycharmProjects\traiding\markets\nyse.csv')


# data = [data_nasdaq, data_nyse]


def parse_ticker(ticker):
    base_url = r'https://money.cnn.com/quote/forecast/forecast.html?symb=' + ticker
    url = urlopen(base_url)
    soup = BeautifulSoup(url, 'html.parser')
    text = ''
    for p in soup.find(id='wsod_forecasts').find_all('p'):
        text += p.text
    pattern = r"""
            (?P<analyst>\d+)
            .*\bmedian\starget\sof\s(?P<median>\d+.\d+)
            .*\shigh\sestimate\sof\s(?P<high>\d+.\d+)
            .*\slow\sestimate\sof\s(?P<low>\d+.\d+)
            .*estimate.*[+|-](?P<change>\d+.\d+)
            .*last\sprice\sof\s(?P<last>\d+.\d+)
            .*is\sto\s(?P<rating>\w+)
    """
    match = re.finditer(pattern, text, flags=re.VERBOSE)
    results = [i.groupdict() for i in match]
    return results


n = len(data_nasdaq)
i = 1
df = pd.DataFrame()
failed = []
names = list(data_nasdaq.iloc[:, 0])

t0 = time()
for ticker in names:
    # print(df)
    try:
        data = parse_ticker(ticker)

        if not data:
            failed.append(ticker)
            continue
        else:
            df = df.append(data, ignore_index=True)

    except Exception as e:
        print(e)
        print(ticker)
        failed.append(ticker)

    print(f'{i} out of {n} completed.')
    i += 1


# print(df)
# print(names)
# print(failed)
for t in failed:
    names.remove(t)

df.index = [names]
df.to_csv('results.csv')

print(time() - t0)

