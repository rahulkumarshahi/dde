
# -*- coding: utf-8 -*-

# Algo options - 1

# For any given day, for any optionable Stock (or index) we have the following:
#   a)  Price of stock with time stamp.
#   b)  Range of interest, e.g., 15% range [0.85 of Stock  to 1.15 of Stock price]
#   c)  Price of options belonging to that range
#   d)  volume of option
#   e)  implied volatility
# The aim is to get all the pertinent options (calls/puts) for all applicable strikes.

#Explanation of code strucutre:
# a) sample-data taken from : https://datashop.cboe.com/option-quotes-intervals-calculations
# file name: UnderlyingOptionsIntervalsCalcs_900sec_2016-06-01.csv
# b) List of underlying (stock or index) price with date and time. 
#    This set has : Once every 15mins. From 09:45AM till 16:15PM
# c) Simplest way was to bundle option data separately from underlying (stock or index) data.
# d) Example :Take the stock price(S) at 9:45AM today. Find lo_S = 0.85*S and hi_S=1.15*S.
# e) Take a list of all option strike price tagged with their expiration date
# f) Use the "closest_hit" logic on lo_S (for PUTs) and hi_S (for CALLs) with the strike_list as reference.
# g) Give the sorted list of all applicable expiration dates and the options data.


import pandas as pd

path = '/Users/rahul/Documents/Python_projects/DDE/'
filename = 'UnderlyingOptionsIntervalsCalcs_900sec_2016-06-01.csv'
file_path = (path + filename).replace('/','//')
option_price = 0.35
underlying_lo = 0.85 # 15% lower than the current price
underlying_hi = 1.15 # 15% higher than the current price


def df_fromfile(file_path=None):
    file_path = (path + filename).replace('/','//')
    return pd.read_csv(file_path, sep=',')

            

def stock_range(S, lo = underlying_lo, hi = underlying_hi):        
    return lo*S, hi*S
    
def datetime_underlying(file_path):
    
    df = df_fromfile(file_path)
    return sorted(list(set(zip(df['quote_datetime']
                               ,(df['underlying_ask']+df['underlying_bid'])/2.0)))
                               ,key= lambda x:x[0])

def datetime_options(file_path):
    
    df = df_fromfile(file_path)
    return sorted(list(set(zip(df['root']
                               ,df['strike']
                               ,df['quote_datetime']
                               ,df['expiration']
                               ,df['option_type']
                               ,df['high']            #why hi and not lo ? as hi gives more realistic price
                               ,df['trade_volume']
                               ,df['implied_volatility'])))
                               ,key= lambda x:x[2])
        
def strike_list(file_path):
    df = df_fromfile(file_path)
    return sorted(list(set(df['strike'])))

def expiration_dates(file_path):
    df = df_fromfile(file_path)
    return sorted(list(set(df['expiration'])))
    
def closest_hit(alist, anum):
    return min(alist, key= lambda x:abs(x-anum))  
        
def ordered_display(anydict):
    from collections import OrderedDict
    d = OrderedDict()
    a = sorted(anydict.keys())
    for k in a:
        d[k] = None
    for k,v in anydict.items():
        d[k] = v
    return d    
    

def get_options_by_expiration(file_path=None, root='VIX',ts='2016-06-01 09:45:00', option_type='C' ):
    """
    Desc: Given a datetime-stamp and expiration, give out the call/put options which 
    are in the underlying's pre-defined low and high range. 
    Input : 
    Output:
    
    """
    d_exp = {}    
    
    lof_strikes = strike_list(file_path)
    
    for t,S in datetime_underlying(file_path):
        if t == ts:
            lo, hi = stock_range(S)
            break
    
    if option_type == 'C':
        closest_call_strike = closest_hit(lof_strikes, hi)
    
    if option_type == 'P':
        closest_put_strike = closest_hit(lof_strikes, lo)
    
    if option_type == 'C':
        for k in datetime_options(file_path):
            if k[0] == root:
                if k[1] == closest_call_strike:
                    if k[2] == ts:
                        if k[4] == option_type:
                            d_exp[k[3]] = "Call, Strike={!s}, hi-price = {!s}, call_vol={!s}, imp_vol={!s}".format(k[1],k[5],k[6], k[7])
        return ordered_display(d_exp)

    if option_type == 'P':
        for k in datetime_options(file_path):        
            if k[0] == root:
                if k[1] == closest_put_strike:
                    if k[2] == ts:
                        if k[4] == option_type:
                            d_exp[k[3]] = "Put, Strike={!s}, hi-price = {!s}, put_vol={!s}, imp_vol={!s}".format(k[1],k[5],k[6], k[7])
                            
        return ordered_display(d_exp)                
   
 
 
   
def main():
    print(get_options_by_expiration())

main()
 


