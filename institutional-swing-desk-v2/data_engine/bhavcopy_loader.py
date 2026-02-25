import requests,zipfile,io,pandas as pd,datetime as dt

def load_oi(date):

    y=date.strftime("%Y")
    m=date.strftime("%b").upper()
    d=date.strftime("%d%b%Y").upper()

    url=f"https://archives.nseindia.com/content/historical/DERIVATIVES/{y}/{m}/fo{d}bhav.csv.zip"

    try:
        r=requests.get(url,headers={"User-Agent":"Mozilla"})
        z=zipfile.ZipFile(io.BytesIO(r.content))

        for n in z.namelist():
            if n.endswith(".csv"):
                df=pd.read_csv(z.open(n))
                return df[df["INSTRUMENT"]=="FUTSTK"]
    except:
        return None