def run():
    today = date.today()
    # reads excel file (must be in the same folder as this file)
    excel = pd.read_excel('inputbb.xlsx', na_filter=False)
    for idx, row in excel.iterrows():
        ticker = row.Ticker
        start_date = row['Start Date']
        end_date = row['End Date']

        # star_date
        # checks if cell is empty
        if len(start_date) == 0:
            start_date = today - relativedelta(years=1)
        # else there is something
        else:
            # long input? DD.MM.YYYY
            if len(start_date) > 6:
                start_date = datetime.strptime(start_date, '%d.%m.%Y')
            else:
                # Smaller input like 60D, 3M
                start_date = get_date(start_date)
        download_date = start_date - relativedelta(years=1)

        # end_date
        # checks if cell is empty
        if len(end_date) == 0:
            end_date = today
        # else there is something
        else:
            # long input? DD.MM.YYYY
            if len(end_date) > 6:
                end_date = datetime.strptime(end_date, '%d.%m.%Y')
            else:
                # Smaller input like 60D, 3M
                end_date = get_date(start_date)



        df = get_price_hist(ticker, download_date, end_date)
        df = get_indicators(df)
        # run plot_chart(data, ticker, plot=True) if you want to see plots (they still will be saved)
        plot_chart(df.loc[start_date:], ticker, plot=True)
