import requests
import json
from decimal import *
import pandas as pd
import operator
import re



def gethitbtc_rates2():
    print "getting Hit BTC rates"
    url = 'https://api.hitbtc.com/api/2/public/ticker'
    resp = requests.get(url=url)
    df = pd.DataFrame(resp.json())
    # print df
    newdf = pd.DataFrame()
    newdf['name'] = df['symbol']
    newdf['hitbtc_buy'] = df['ask']
    newdf['hitbtc_sell'] = df['bid']
    print "geot Hit BTC rates"
    return newdf

def getidex_rates2():
    print "getting idex rates"
    url = 'https://api.idex.market/returnTicker'
    datatocheck = {}
    returndata = []
    resp = requests.post(url=url, data=json.dumps(datatocheck))
    keys = resp.json().keys()
    for each in keys:
        data = {}
        # print resp.json()[each]['lowestAsk']
        if resp.json().get(each) is not None:
            if each.split('_')[0] == "ETH":
                if resp.json()[each]['lowestAsk'] != "N/A" and resp.json()[each]['highestBid'] != "N/A":
                    data['symbol'] = "".join(each.split('_')[::-1])
                    data['ask'] = resp.json()[each]['lowestAsk']
                    data['bid'] = resp.json()[each]['highestBid']
                    returndata.append(data)
    df = pd.DataFrame(returndata)
    newdf = pd.DataFrame()
    newdf['name'] = df['symbol']
    newdf['idex_buy'] = df['ask']
    newdf['idex_sell'] = df['bid']
    print "got idex rates"
    return newdf

def getbinance_rates2():
    print "getting binance rates"
    url = 'https://api.binance.com/api/v3/ticker/bookTicker'
    resp = requests.get(url=url)
    # print resp
    df = pd.DataFrame(resp.json())
    # print df
    newdf = pd.DataFrame()
    newdf['name'] = df['symbol']
    newdf['binance_buy'] = df['askPrice']
    newdf['binance_sell'] = df['bidPrice']
    print "got binance rates"
    return newdf

def tidex_get_all_pairs():
    print "getting tidex rates"
    returndata = []
    url = 'https://api.tidex.com/api/3/info'
    resp = requests.get(url=url)
    data = resp.json()['pairs'].keys()
    final_pair = ''
    for each in data:
        if final_pair == '':
            final_pair = each
        else:
            final_pair = final_pair + '-' + each
    url2 = 'https://api.tidex.com/api/3/ticker/'+ str(final_pair) + '?ignore_invalid=1'
    resp2 = requests.get(url=url2)
    for key, value in resp2.json().items():
        inddata = {}
        inddata['name'] = (key.split('_')[0]+ key.split('_')[1]).upper()
        inddata['tidex_buy'] = value['sell']
        inddata['tidex_sell'] = value['buy']
        returndata.append(inddata)
    print "got tidex rates"
    return pd.DataFrame(returndata)

def getcoindelta_rates():
    print "getting coindelta rates"
    url = 'https://coindelta.com/api/v1/public/getticker/'
    resp = requests.get(url=url)
    df = pd.DataFrame(resp.json())
    newdf = pd.DataFrame()
    newdf['name'] = df['MarketName'].apply(lambda x: (str(x).split('-')[0] + str(x).split('-')[1]).upper())
    newdf['coindelta_buy'] = df['Ask']
    newdf['coindelta_sell'] = df['Bid']
    print "got coindelta rates"
    return newdf

def getcryptopia_rates():
    print "getting cryptopia rates"
    url = 'https://www.cryptopia.co.nz/api/GetMarkets'
    resp = requests.get(url=url)
    df = pd.DataFrame(resp.json()['Data'])
    newdf = pd.DataFrame()
    newdf['name'] = df['Label'].apply(lambda x: (str(x).split('/')[0] + str(x).split('/')[1]))
    newdf['cryptopia_buy'] = df['AskPrice']
    newdf['cryptopia_sell'] = df['BidPrice']
    print "got coindelta rates"
    return newdf





def bittrex_get_rates(marketname):
    data = {}
    try:
        url = 'https://bittrex.com/api/v1.1/public/getticker?market=' + str(marketname)
        resp = requests.get(url=url)
        print marketname
        print resp.json()
        if resp.json()['result'] is not None and resp.json()['result']['Bid'] is not None and resp.json()['result']['Ask'] is not None:
            print resp.json()['result']
            data['name'] = "".join(marketname.split('-')[::-1])
            data['bittrex_bid'] = resp.json()['result']['Bid']
            data['bittrex_ask'] = resp.json()['result']['Ask']
            print data
        return data
    except:
        return data











def polinex_rates():
    returndata = []
    url = 'https://poloniex.com/public?command=returnTicker'
    resp = requests.get(url=url)
    print resp.json()
    for key, value in resp.json().items():
        inddata = {}
        inddata['name'] = (key.split('_')[1]+ key.split('_')[0])
        inddata['polinex_buy'] = value['lowestAsk']
        inddata['polinex_sell'] = value['highestBid']
        returndata.append(inddata)
    return pd.DataFrame(returndata)

def quoinex_rates():
    url = 'https://api.qryptos.com/products'
    resp = requests.get(url=url)
    df = pd.DataFrame(resp.json())
    df = df[(df.disabled == False)]
    newdf = pd.DataFrame()
    newdf['name'] = df['currency_pair_code']
    newdf['quoinex_buy'] = df['AskPrice']
    newdf['quoinex_sell'] = df['BidPrice']
    return newdf


def bittrex_symbols2():
    calltomake = []
    returndata = []
    url = 'https://bittrex.com/api/v1.1/public/getmarkets'
    resp = requests.get(url=url)
    for each in resp.json()['result']:
        # calltomake.append(each['MarketName'])
        # print each['MarketName']
        if each['BaseCurrencyLong'] == 'Ethereum' or each['BaseCurrencyLong'] == 'Bitcoin':
            calltomake.append(each['MarketName'])
    from concurrent.futures import ThreadPoolExecutor, wait, as_completed
    pool = ThreadPoolExecutor(20)
    futures = [pool.submit(bittrex_get_rates, calls) for calls in calltomake]
    for r in as_completed(futures):
        final_received_data = r.result()
        returndata.append(final_received_data)
    df = pd.DataFrame(returndata)
    newdf = pd.DataFrame()
    newdf['name'] = df['name']
    newdf['bittrex_buy'] = df['bittrex_ask']
    newdf['bittrex_sell'] = df['bittrex_bid']
    return newdf

def get_all_price2():
    print "starting to get rates"
    returndata = []
    hitbtc_data = gethitbtc_rates2()
    binance_data = getbinance_rates2()
    idex_data = getidex_rates2()
    tidex_data = tidex_get_all_pairs()
    coindelta_data = getcoindelta_rates()
    cryptopia_data = getcryptopia_rates()
    bittrex_data = bittrex_symbols2()
    merged_outer = pd.merge(left=hitbtc_data, right=binance_data, how='outer', left_on='name', right_on='name')
    merged_outer = pd.merge(left=merged_outer, right=idex_data, how='outer', left_on='name', right_on='name')
    merged_outer = pd.merge(left=merged_outer, right=tidex_data, how='outer', left_on='name', right_on='name')
    merged_outer = pd.merge(left=merged_outer, right=coindelta_data, how='outer', left_on='name', right_on='name')
    merged_outer = pd.merge(left=merged_outer, right=cryptopia_data, how='outer', left_on='name', right_on='name')
    merged_outer = pd.merge(left=merged_outer, right=bittrex_data, how='outer', left_on='name', right_on='name')

    df = merged_outer.where((pd.notnull(merged_outer)), None)

    df['hitbtc_buy-bittrex_sell'] = df.apply(lambda row: profit(row['hitbtc_buy'], row['bittrex_sell']), axis=1)
    df['binance_buy-bittrex_sell'] = df.apply(lambda row: profit(row['binance_buy'], row['bittrex_sell']), axis=1)
    df['idex_buy-bittrex_sell'] = df.apply(lambda row: profit(row['idex_buy'], row['bittrex_sell']), axis=1)
    df['tidex_buy-bittrex_sell'] = df.apply(lambda row: profit(row['tidex_buy'], row['bittrex_sell']), axis=1)
    df['coindelta_buy-bittrex_sell'] = df.apply(lambda row: profit(row['coindelta_buy'], row['bittrex_sell']), axis=1)
    df['cryptopia_buy-bittrex_sell'] = df.apply(lambda row: profit(row['cryptopia_buy'], row['bittrex_sell']), axis=1)

    df['bittrex_buy-hitbtc_sell'] = df.apply(lambda row: profit(row['bittrex_buy'], row['hitbtc_sell']), axis=1)
    df['bittrex_buy-binance_sell'] = df.apply(lambda row: profit(row['bittrex_buy'], row['binance_sell']), axis=1)
    df['bittrex_buy-idex_sell'] = df.apply(lambda row: profit(row['bittrex_buy'], row['idex_sell']), axis=1)
    df['bittrex_buy-tidex_sell'] = df.apply(lambda row: profit(row['bittrex_buy'], row['tidex_sell']), axis=1)
    df['bittrex_buy-coindelta_sell'] = df.apply(lambda row: profit(row['bittrex_buy'], row['coindelta_sell']), axis=1)
    df['bittrex_buy-cryptopia_sell'] = df.apply(lambda row: profit(row['bittrex_buy'], row['cryptopia_sell']), axis=1)





    df['hitbtc_buy-binance_sell'] = df.apply(lambda row: profit(row['hitbtc_buy'], row['binance_sell']), axis=1)
    df['hitbtc_buy-idex_sell'] = df.apply(lambda row: profit(row['hitbtc_buy'], row['idex_sell']), axis=1)
    df['hitbtc_buy-tidex_sell'] = df.apply(lambda row: profit(row['hitbtc_buy'], row['tidex_sell']), axis=1)
    df['hitbtc_buy-coindelta_sell'] = df.apply(lambda row: profit(row['hitbtc_buy'], row['coindelta_sell']), axis=1)
    df['hitbtc_buy-cryptopia_sell'] = df.apply(lambda row: profit(row['hitbtc_buy'], row['cryptopia_sell']), axis=1)


    df['binance_buy-hitbtc_sell'] = df.apply(lambda row: profit(row['binance_buy'], row['hitbtc_sell']), axis=1)
    df['binance_buy-idex_sell'] = df.apply(lambda row: profit(row['binance_buy'], row['idex_sell']), axis=1)
    df['binance_buy-tidex_sell'] = df.apply(lambda row: profit(row['binance_buy'], row['tidex_sell']), axis=1)
    df['binance_buy-coindelta_sell'] = df.apply(lambda row: profit(row['binance_buy'], row['coindelta_sell']), axis=1)
    df['binance_buy-cryptopia_sell'] = df.apply(lambda row: profit(row['binance_buy'], row['cryptopia_sell']), axis=1)

    df['idex_buy-hitbtc_sell'] = df.apply(lambda row: profit(row['idex_buy'], row['hitbtc_sell']), axis=1)
    df['idex_buy-binance_sell'] = df.apply(lambda row: profit(row['idex_buy'], row['binance_sell']), axis=1)
    df['idex_buy-tidex_sell'] = df.apply(lambda row: profit(row['idex_buy'], row['tidex_sell']), axis=1)
    df['idex_buy-coindelta_sell'] = df.apply(lambda row: profit(row['idex_buy'], row['coindelta_sell']), axis=1)
    df['idex_buy-cryptopia_sell'] = df.apply(lambda row: profit(row['idex_buy'], row['cryptopia_sell']), axis=1)

    df['tidex_buy-hitbtc_sell'] = df.apply(lambda row: profit(row['tidex_buy'], row['hitbtc_sell']), axis=1)
    df['tidex_buy-binance_sell'] = df.apply(lambda row: profit(row['tidex_buy'], row['binance_sell']), axis=1)
    df['tidex_buy-idex_sell'] = df.apply(lambda row: profit(row['tidex_buy'], row['idex_sell']), axis=1)
    df['tidex_buy-coindelta_sell'] = df.apply(lambda row: profit(row['tidex_buy'], row['coindelta_sell']), axis=1)
    df['tidex_buy-cryptopia_sell'] = df.apply(lambda row: profit(row['tidex_buy'], row['cryptopia_sell']), axis=1)

    df['coindelta_buy-hitbtc_sell'] = df.apply(lambda row: profit(row['coindelta_buy'], row['hitbtc_sell']), axis=1)
    df['coindelta_buy-binance_sell'] = df.apply(lambda row: profit(row['coindelta_buy'], row['binance_sell']), axis=1)
    df['coindelta_buy-idex_sell'] = df.apply(lambda row: profit(row['coindelta_buy'], row['idex_sell']), axis=1)
    df['coindelta_buy-tidex_sell'] = df.apply(lambda row: profit(row['coindelta_buy'], row['tidex_sell']), axis=1)
    df['coindelta_buy-cryptopia_sell'] = df.apply(lambda row: profit(row['coindelta_buy'], row['cryptopia_sell']), axis=1)

    df['cryptopia_buy-hitbtc_sell'] = df.apply(lambda row: profit(row['cryptopia_buy'], row['hitbtc_sell']), axis=1)
    df['cryptopia_buy-binance_sell'] = df.apply(lambda row: profit(row['cryptopia_buy'], row['binance_sell']), axis=1)
    df['cryptopia_buy-idex_sell'] = df.apply(lambda row: profit(row['cryptopia_buy'], row['idex_sell']), axis=1)
    df['cryptopia_buy-tidex_sell'] = df.apply(lambda row: profit(row['cryptopia_buy'], row['tidex_sell']), axis=1)
    df['cryptopia_buy-coindelta_sell'] = df.apply(lambda row: profit(row['cryptopia_buy'], row['coindelta_sell']),axis=1)

    transactions = ['hitbtc_buy-bittrex_sell','binance_buy-bittrex_sell','idex_buy-bittrex_sell','tidex_buy-bittrex_sell','coindelta_buy-bittrex_sell','cryptopia_buy-bittrex_sell','bittrex_buy-hitbtc_sell','bittrex_buy-binance_sell','bittrex_buy-idex_sell','bittrex_buy-tidex_sell','bittrex_buy-coindelta_sell','bittrex_buy-cryptopia_sell','hitbtc_buy-binance_sell','hitbtc_buy-idex_sell','hitbtc_buy-tidex_sell','hitbtc_buy-coindelta_sell','hitbtc_buy-cryptopia_sell','binance_buy-hitbtc_sell','binance_buy-idex_sell','binance_buy-tidex_sell','binance_buy-coindelta_sell','binance_buy-cryptopia_sell','idex_buy-hitbtc_sell','idex_buy-binance_sell','idex_buy-tidex_sell','idex_buy-coindelta_sell','idex_buy-cryptopia_sell','tidex_buy-hitbtc_sell','tidex_buy-binance_sell','tidex_buy-idex_sell','tidex_buy-coindelta_sell','tidex_buy-cryptopia_sell','coindelta_buy-hitbtc_sell','coindelta_buy-binance_sell','coindelta_buy-idex_sell','coindelta_buy-tidex_sell','coindelta_buy-cryptopia_sell','cryptopia_buy-hitbtc_sell','cryptopia_buy-binance_sell','cryptopia_buy-idex_sell','cryptopia_buy-tidex_sell','cryptopia_buy-coindelta_sell']
    for index, row in df.iterrows():
        for each in transactions:
            if row[each] is not None:
                try:
                    data = datatoreturn(row,each)
                    returndata.append(data)
                except Exception as e:
                    print e
    return returndata


def profit(x,y):
    try:
        if x is not None and y is not None:
            return Decimal(Decimal(y)-Decimal(x))
        else:
            return None
    except:
        return None

def datatoreturn(row,transaction):
    data = {}
    data['name'] = row['name']
    data['transaction'] = transaction
    data['buy_rate'] = row[transaction.split('-')[0]]
    data['sell_rate'] = row[transaction.split('-')[1]]
    data['profit'] = row[transaction]
    data['profit_raio'] = Decimal(Decimal(row[transaction])/Decimal(row[transaction.split('-')[0]]))
    return data


def sendemail(data):
    from django.core.mail import EmailMessage
    name = data.get("name")
    email = data.get("email")
    phone = data.get("contact")
    message = data['message']
    email = EmailMessage(name, message, to=['n.bhawsinka@gmail.com'])
    email.send()



