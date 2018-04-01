#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
from config import config
import pandas as pd


def merge_and_sum(*dicts):
    ret = defaultdict(int)
    for d in dicts:
        for k, v in d.items():
            ret[k] += v
    return dict(ret)


def get_overall_balances(portfolio):
    balances = {}
    if 'amounts' in portfolio:
        balances = merge_and_sum(balances, {k.upper(): v for k, v in portfolio_config['amounts'].items()})
    if 'wallets' in portfolio:
        pass
    if 'exchanges' in portfolio:
        pass
    return balances


if __name__ == '__main__':
    # print(config)
    # exit(0)

    limit = 5  # only load the top 200 currencies, if you have invested in smaller ones increase this limit
    coin_market_cap_api = 'https://api.coinmarketcap.com/v1/ticker/?limit={}'.format(limit)
    # print(coin_market_cap_api)
    now = pd.datetime.now()
    market_data = pd.read_json(coin_market_cap_api)
    # print(market_data.head(10))

    for portfolio_name, portfolio_config in config['portfolios'].items():
        balances = get_overall_balances(portfolio_config)

        # display your blockfolio
        block_folio = pd.DataFrame(list(balances.items()), columns=['symbol', 'amount'])
        # print(block_folio)
        # print(block_folio.head(len(block_folio)))

        # merge the API and blockfolio data and sort by investment value
        merged_data = block_folio.merge(market_data, how='left')
        merged_data['value_usd'] = merged_data.amount * merged_data.price_usd
        merged_data['coinshare'] = merged_data.amount / merged_data.available_supply
        merged_data = merged_data.sort_values('value_usd', ascending=False)
        # print(merged_data.head())

        networth = 'Your {} portfolio is currently (i.e {}) worth {:.2f} USD!'.format(portfolio_name,
                                                                                      now.strftime('%Y-%m-%d %I:%M %p'),
                                                                                      merged_data.value_usd.sum())
        print(networth)
