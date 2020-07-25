import pandas as pd
import os.path
from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))

# Data Preprocessing & Creating Files joining SPY, BTC, VIX

def pre(ask_df, bid_df):
    df = pd.DataFrame()
    df["Gmt time"] = bid_df["Gmt time"]
    df["Bid"] = bid_df["Close"]
    df["Ask"] = ask_df["Close"]
    df["Gmt time"] = pd.to_datetime(df["Gmt time"], format="%d.%m.%Y %H:%M:%S.%f")
    df["Midprice"] = (df["Ask"] + df["Bid"])/2
    return df

def subset(df, df_2):
    df = df[df["Gmt time"].isin(df_2["Gmt time"])]
    df = df.reset_index()
    df.drop(columns=["index"], inplace=True)
    return df

def create_df(BTC_df, SPY_df, VIX_df):
    df = pd.DataFrame()
    df["Gmt time"] = BTC_df["Gmt time"]
    df["BTC_Bid"] = BTC_df["Bid"]
    df["BTC_Ask"] = BTC_df["Ask"]
    df["BTC_Midprice"] = BTC_df["Midprice"]
    df["SPY_Bid"] = SPY_df["Bid"]
    df["SPY_Ask"] = SPY_df["Ask"]
    df["SPY_Midprice"] = SPY_df["Midprice"]
    df["VIX_Bid"] = VIX_df["Bid"]
    df["VIX_Ask"] = VIX_df["Ask"]
    df["VIX_Midprice"] = VIX_df["Midprice"]
    return df

def df_compile(month):
    try:
        SPY_folder = r"C:\\Users\\jmsda\\Documents\\Crypto Project\\Dukascopy\\SPY\\" + month
        BTC_folder = SPY_folder.replace("SPY", "Bitcoin")
        VIX_folder = SPY_folder.replace("SPY", "VIX")

        datelist_ = []
        for i in os.listdir(VIX_folder):
            datelist_.append(i[-14:])    
        datelist = list(set(datelist_))

        filelist = []
        for i in os.listdir(VIX_folder):
            filelist.append(i)
        for j in os.listdir(SPY_folder):
            filelist.append(j)
        for k in os.listdir(BTC_folder):
            filelist.append(k)

        for j in datelist:
            for i in filelist:
                if j in i:
                    if "SPY" in i:
                        if "BID" in i:
                            SPY_bid = pd.read_csv(SPY_folder + i, encoding = "utf-8", engine='python')
                        if "ASK" in i:
                            SPY_ask = pd.read_csv(SPY_folder + i, encoding = "utf-8", engine='python')
                    elif "BTC" in i:
                        if "BID" in i:
                            BTC_bid = pd.read_csv(BTC_folder + i, encoding = "utf-8", engine='python')
                        if "ASK" in i:
                            BTC_ask = pd.read_csv(BTC_folder + i, encoding = "utf-8", engine='python')
                    elif "VXX" in i:
                        if "BID" in i:
                            VIX_bid = pd.read_csv(VIX_folder + i, encoding = "utf-8", engine='python')
                        if "ASK" in i:
                            VIX_ask = pd.read_csv(VIX_folder + i, encoding = "utf-8", engine='python') 
                else:
                    pass

            BTC_df = pre(BTC_ask, BTC_bid)
            SPY_df = pre(SPY_ask, SPY_bid)
            VIX_df = pre(VIX_ask, VIX_bid)

            BTC_df = subset(BTC_df, SPY_df)
            SPY_df = subset(SPY_df, BTC_df)
            VIX_df = subset(VIX_df, SPY_df)
            SPY_df = subset(SPY_df, VIX_df)
            BTC_df = subset(BTC_df, SPY_df)

            df = create_df(BTC_df, SPY_df, VIX_df)
            df_name = r"C:\\Users\\jmsda\\Documents\\Crypto Project\\Dukascopy\\df\\" + month + "df" + str(j)
            df.to_csv(df_name, encoding = "utf-8")
            
    except Exception as e:
        print("Error in file: ", j)
        print(e)
        
