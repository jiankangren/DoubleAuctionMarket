import spot_system as sys
import random
import csv
import matplotlib.pyplot as plt
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go
import os
'''This program is a condensed version of spot_system to build the periods of trading'''

'''There could be a problem in counting traders... when run this program shows 10 traders 
when the input file only has 8'''

class SpotMarketPeriod(object):
    def __init__(self, session_name, num_periods):  # creates name and number of periods for market

        self.display = True
        self.session_name = session_name

        self.period = 0
        self.num_periods = num_periods
        self.num_buyers = 4  # number of buyers
        self.num_sellers = 4  # number of sellers
        self.limits = (999, 0)  # ceiling and floor for bidding
        self.num_market_periods = 100  # number of periods auction run
        self.trader_names = []
        self.traders = []
        self.trader_info = {}
        self.sys = sys.SpotSystem()  # calls SpotSystem() which prepares market and traders

    def init_spot_system(self, name, limits, rounds, input_path, input_file):
        self.sys.init_spot_system(name, limits, rounds, input_path, input_file)

    def init_traders(self, trader_names):
        self.sys.init_traders(trader_names)

    def run(self):
        self.sys.run()

    def eval(self):
        return self.sys.eval()  # runs eval method from spot_system

    def run_period(self, period, header):
        self.period = period
        self.run()

    def save_period(self, results):
        pass

'''This program iterates through the number of rounds'''
if __name__ == "__main__":
    num_periods = 5
    limits = (999, 0)
    rounds = 100
    name = "trial"
    period = 1
    session_name = "session_test"
    header = session_name

    smp = SpotMarketPeriod(session_name, num_periods)

    '''This will change when we create more programmed agents to add into the model'''

    # Put Trader Class Names Here - note traders strategy is named trader class name
    zi = "ZeroIntelligenceTrader"
    si = "SimpleTrader"
    trader_names = [zi, si, zi, si, zi, si, zi, si]  # Order of trader strategies in generic trader array
    # input - output and display options
    input_path = "C:\\Users\\Summer17\\Desktop\\Repos\\DoubleAuctionMisc\\projects\\"
    input_file = "TEST"
    output_path = "C:\\Users\\Summer17\\Desktop\\Repos\\DoubleAuctionMisc\\data\\"
    header = session_name
    smp.init_spot_system(name, limits, rounds, input_path, input_file)
    rnd_traders = trader_names    # because shuffle shuffels the list in place, returns none
    eff = []
    periods_list = []
    act_surplus = []
    maxi_surplus = []
    earns = []
    for k in range(num_periods):
        earns.append([[], []])
    print(earns)
    n = 0
    file_check = os.path.isfile('./Experiment' + str(n) + '.csv')  # TODO check files and create new one
    output_file = open('Experiment' + str(n) + '.csv', 'w', newline='')
    t = 0
    for k in range(num_periods):
        periods_list.append(k)
        random.shuffle(rnd_traders)  # reassign traders each period
        print(rnd_traders)
        smp.init_traders(rnd_traders)
        print("**** Running Period {}".format(k))
        smp.run_period(period, header)
        results = smp.eval()
        eff.append(results[8])
        act_surplus.append(results[7])
        maxi_surplus.append(results[6])
        output_writer = csv.writer(output_file)
        output_writer.writerow(results)
        t = t + 1
        print(results)
    output_file.close()

    print("Market Efficiencies:" + str(eff))
    print("Actual Surpluses:" + str(act_surplus))
    print("Maximum Surpluses:" + str(maxi_surplus))

    with plt.style.context('seaborn-dark-palette'):  # added a plot of the market efficiencies
        x = np.array(periods_list)
        y = np.array(eff)
        plt.plot(x, y, marker='s')
        plt.title("Market Efficiencies")
        plt.xlabel("Period")
        plt.ylabel("Efficiency (%)")
        plt.grid(True)
        plt.show()

    '''with plt.style.context('seaborn-dark-palette'):  # added a plot of the market efficiencies
        x = np.array(periods_list)
        y1 = np.array(act_surplus)
        y2 = np.array(maxi_surplus)
        plt.plot(x, y1)
        plt.plot(x, y2)
        plt.title("Market Surpluses")
        plt.xlabel("Period")
        plt.ylabel("Surplus")
        plt.grid(True)
        plt.show()'''
    trace1 = go.Scatter(
        x=np.array(periods_list),
        y=np.array(act_surplus), name='Actual Surplus')
    trace2 = go.Scatter(
        x=np.array(periods_list),
        y=np.array(maxi_surplus), name='Max Surplus')
    data = [trace1, trace2]
    layout = go.Layout(title='Market Surpluses by Period',
                       xaxis=dict(title='Periods',
                                  titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')),
                       yaxis=dict(title='Surplus (units)',
                                  titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')))
    fig = go.Figure(data=data, layout=layout)
    py.offline.plot(fig)


    # TODO create graphs of average earnings per period