import pickle
from xbbg import blp

if __name__ == '__main__':
    single_ticker = ['NVDA US Equity']
    multi_ticker = ['NVDA US Equity', 'AAPL US Equity']
    single_field = ['PX_LAST']
    multi_field = ['PX_LAST', 'PX_VOLUME']
    data = {'errors': []}
    try:
        df = blp.bdh(tickers=multi_ticker, flds=multi_field, start_date='2021-09-20')
        data['bdh_mm_wsd'] = df
    except Exception as e:
        data['errors'].append(['bdh_mm_wsd', e])
    try:
        df = blp.bdh(tickers=multi_ticker, flds=multi_field)
        data['bdh_mm_wosd'] = df
    except Exception as e:
        data['errors'].append(['bdh_mm_wosd', e])

    try:
        df = blp.bdp(tickers=multi_ticker, flds=multi_field)
        data['bdp_mm'] = df
    except Exception as e:
        data['errors'].append(['bdp_mm', e])
    try:
        df = blp.bds(tickers=multi_ticker, flds=multi_field)
        data['bds_mm'] = df
    except Exception as e:
        data['errors'].append(['bds_mm', e])

    blp.bdp()
    blp.bds()
    # data = {'errors': []}
    # fields = ['PX_LAST', 'PX_P/B', 'PX_MID', 'BEST_PE', 'R9083', 'PX_VOLUME',
    #           ['PX_LAST', 'PX_VOLUME'], ['BEST_PE_RATIO', 'BEST_FPERIOD_OVERRIDE']]
    # for fld in fields:
    #     try:
    #         df = blp.bdh(tickers='SPX Index', flds=fld)
    #         data[fld + '_today'] = df[fld]
    #     except Exception as e:
    #         data['errors'].append([fld + '_today', e])
    #     try:
    #         df = blp.bdh(tickers='SPX Index', flds=fld, start_date='2021-09-20')
    #         data[fld + '_days_ago'] = df
    #     except Exception as e:
    #         data['errors'].append([fld + '_days_ago', e])
    #
    # # multiple tickers single field
    # tickers = ['NVDA US Equity', 'AAPL US Equity']
    # single_field = ['Close']
    # multiple_fields = ['High', 'Low', 'Last_Price']
    # try:
    #     df = blp.bdh(tickers=tickers, flds=single_field)
    #     data['two_tickers_single'] = df
    # except Exception as e:
    #     data['errors'].append(['two_tickers_single', e])
    #
    # try:
    #     df = blp.bdh(tickers=tickers, flds=single_field, start_date='2021-09-20')
    #     data['two_tickers_single_days_ago'] = df
    # except Exception as e:
    #     data['errors'].append(['two_tickers_single_days_ago', e])
    #
    # # multiple tickers, multiple fields entries
    # try:
    #     df = blp.bdh(['NVDA US Equity', 'AAPL US Equity'], flds=['High', 'Close'])
    #     data['two_tickers_multi'] = df
    # except Exception as e:
    #     data['errors'].append(['two_tickers_multi', e])
    #
    # try:
    #     df = blp.bdh(['NVDA US Equity', 'AAPL US Equity'], flds=['High', 'Close'], start_date='2021-09-20')
    #     data['two_tickers_multi_days_ago'] = df
    # except Exception as e:
    #     data['errors'].append(['two_tickers_multi_days_ago', e])
    #
    # with open('data.pkl', 'wb') as f:
    #     pickle.dump(data, f)
