
def run():
    # Get today's date
    today = date.today()

    # Read excel file (must be in the same folder as this file)
    df = pd.read_excel('inputbb.xlsx', dtype={'Start Date': datetime, 'End Date': datetime}, nrows=7)

    # replaces all spaces in column Start Date and End Date with today's date
    df.replace({'Start Date': {'\s+': datetime.today().date()},
                'End Date': {'\s+': datetime.today().date()}}, inplace=True, regex=True)
    # replaces all NaT or NaN with today's date
    df.replace({pd.NaT: datetime.today().date()}, inplace=True)

    for idx, row in df.iterrows():
        ticker = row.Ticker
        start_date = row['Start Date']
        end_date = row['End Date']

        # Start date is year ago by a default (empty cell in excel)
        if start_date == today:
            start_date = today - relativedelta(years=1)
        else:
            # if start date is not today, there was something in a cell
            # if it was a date - we fine, if not (4d / 10m / 5y/ ytd) need to convert it
            if not isinstance(start_date, datetime):
                start_date = get_date(start_date)

        # download date is different, we get extra year of data to plot indicators
        download_date = start_date - relativedelta(years=1)

        # End date is today by a default (empty cell in excel)
        if end_date != today:
            # if it is not today's date then there was something in a cell
            # if it was a date - we fine, if not (4d / 10m / 5y/ ytd) need to convert it
            if not isinstance(end_date, datetime):
                end_date = get_date(end_date)

        df = get_price_hist(ticker, download_date, end_date)
        df = get_indicators(df)
        # run plot_chart(data, ticker, plot=True) if you want to see plots (they still will be saved)
        plot_chart(df.loc[start_date:], ticker, plot=True)