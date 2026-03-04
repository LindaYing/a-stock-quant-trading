"""
简化版双均线策略 - 不依赖 matplotlib
"""

import pandas as pd
import numpy as np
from datetime import datetime


class SimpleMAStrategy:
    """简化版双均线策略"""
    
    def __init__(self, short_period=5, long_period=20):
        self.short_period = short_period
        self.long_period = long_period
        self.name = f"MA{short_period}_{long_period}"
    
    def calculate_signals(self, df):
        """计算交易信号"""
        data = df.copy()
        
        # 计算均线
        data['ma_short'] = data['close'].rolling(window=self.short_period).mean()
        data['ma_long'] = data['close'].rolling(window=self.long_period).mean()
        
        # 生成信号
        data['signal'] = 0
        
        # 金叉
        data.loc[
            (data['ma_short'] > data['ma_long']) & 
            (data['ma_short'].shift(1) <= data['ma_long'].shift(1)),
            'signal'
        ] = 1
        
        # 死叉
        data.loc[
            (data['ma_short'] < data['ma_long']) & 
            (data['ma_short'].shift(1) >= data['ma_long'].shift(1)),
            'signal'
        ] = -1
        
        data['position'] = data['signal'].replace(0, np.nan).ffill().fillna(0)
        
        return data
    
    def backtest(self, df, initial_capital=100000, commission=0.0003):
        """回测策略"""
        data = self.calculate_signals(df)
        
        capital = initial_capital
        position = 0
        trades = []
        
        for i in range(len(data)):
            row = data.iloc[i]
            
            if row['signal'] == 1 and position == 0:
                # 计算可买股数（考虑手续费）
                shares = int(capital / (row['close'] * (1 + commission)))
                cost = shares * row['close'] * (1 + commission)
                
                if shares > 0 and cost <= capital:
                    position = shares
                    capital -= cost
                    trades.append({
                        'date': row.name,
                        'action': 'BUY',
                        'price': row['close'],
                        'shares': shares,
                        'cost': cost,
                        'capital': capital
                    })
            
            elif row['signal'] == -1 and position > 0:
                revenue = position * row['close'] * (1 - commission)
                capital += revenue
                
                trades.append({
                    'date': row.name,
                    'action': 'SELL',
                    'price': row['close'],
                    'shares': position,
                    'revenue': revenue,
                    'capital': capital
                })
                
                position = 0
        
        if position > 0:
            last_price = data.iloc[-1]['close']
            revenue = position * last_price * (1 - commission)
            capital += revenue
            trades.append({
                'date': data.index[-1],
                'action': 'SELL',
                'price': last_price,
                'shares': position,
                'revenue': revenue,
                'capital': capital
            })
        
        final_value = capital
        total_return = (final_value - initial_capital) / initial_capital * 100
        buy_hold_return = (data.iloc[-1]['close'] - data.iloc[0]['close']) / data.iloc[0]['close'] * 100
        
        # 计算最大回撤
        data['strategy_value'] = initial_capital
        current_capital = initial_capital
        current_position = 0
        
        for i in range(len(data)):
            row = data.iloc[i]
            if row['signal'] == 1 and current_position == 0:
                shares = int(current_capital / (row['close'] * (1 + commission)))
                if shares > 0:
                    current_position = shares
                    current_capital -= shares * row['close'] * (1 + commission)
            elif row['signal'] == -1 and current_position > 0:
                current_capital += current_position * row['close'] * (1 - commission)
                current_position = 0
            
            if current_position > 0:
                data.loc[data.index[i], 'strategy_value'] = current_capital + current_position * row['close']
            else:
                data.loc[data.index[i], 'strategy_value'] = current_capital
        
        data['cummax'] = data['strategy_value'].cummax()
        data['drawdown'] = (data['strategy_value'] - data['cummax']) / data['cummax'] * 100
        max_drawdown = data['drawdown'].min()
        
        num_trades = len([t for t in trades if t['action'] == 'BUY'])
        
        winning_trades = 0
        for i in range(0, len(trades)-1, 2):
            if i+1 < len(trades):
                buy_price = trades[i]['price']
                sell_price = trades[i+1]['price']
                if sell_price > buy_price:
                    winning_trades += 1
        
        win_rate = (winning_trades / num_trades * 100) if num_trades > 0 else 0
        
        return {
            'initial_capital': initial_capital,
            'final_value': final_value,
            'total_return': total_return,
            'buy_hold_return': buy_hold_return,
            'max_drawdown': max_drawdown,
            'num_trades': num_trades,
            'win_rate': win_rate,
            'trades': trades,
            'trades_df': pd.DataFrame(trades),
            'data': data
        }
