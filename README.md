# Scraper for Market Science Reports

**Run python scraper.py and reports are going to be scanned backwards, starting with today.**

**Results are saved in marketssci.csv**

**How To Use Scraped data:**
```python
def some_main():
    df = pd.read_csv("marketssci.csv")
    print(df)
```

**In case you nead to clear csv, don't remove the first row (headers) from the csv file**

_For a moment this scraper was meant to be generic, but in the end it isn't._
