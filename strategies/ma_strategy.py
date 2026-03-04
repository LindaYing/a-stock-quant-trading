"""
双均线策略 (Moving Average Crossover Strategy)

策略逻辑:
- 当短期均线上穿长期均线时，买入 (金叉)
- 当短期均线下穿长期均线时，卖出 (死叉)

参数:
- short_period: 短期均线周期，默认 5 天
- long_period: 长期均线周期，默认 20 天
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False


class MAStrategy:
    """双均线策略"""
    
    def __init__(self, short_period=5, long_period=20):
        """
        初始化策略
        
        Args:
            short_period: 短期均线周期
            long_period: 长期均线周期
        """
        self.short_period = short_period
        self.long_period = long_period
        self.name = f"MA{short_period}_{long_period}"
    
    def calculate_signals(self, df):
        """
        计算交易信号
        
        Args:
            df: 包含 close 列的 DataFrame
        
        Returns:
            DataFrame: 添加了信号列的数据
        """
        # 复制数据
        data = df.copy()
        
        # 计算均线
        data['ma_short'] = data['close'].rolling(window=self.short_period).mean()
        data['ma_long'] = data['close'].rolling(window=self.long_period).mean()
        
        # 生成信号
        # 1: 买入, -1: 卖出, 0: 持有
        data['signal'] = 0
        
        # 金叉: 短期均线上穿长期均线
        data.loc[
            (data['ma_short'] > data['ma_long']) & 
            (data['ma_short'].shift(1) <= data['ma_long'].shift(1)),
            'signal'
        ] = 1
        
        # 死叉: 短期均线下穿长期均线
        data.loc[
            (data['ma_short'] < data['ma_long']) & 
            (data['ma_short'].shift(1) >= data['ma_long'].shift(1)),
            'signal'
        ] = -1
        
        # 持仓状态: 1 持有, 0 空仓
        data['position'] = data['signal'].replace(0, np.nan).ffill().fillna(0)
        
        return data
    
    def backtest(self, df, initial_capital=100000, commission=0.0003):
        """
        回测策略
        
        Args:
            df: 股票数据
            initial_capital: 初始资金
            commission: 手续费率
        
        Returns:
            dict: 回测结果
        """
        # 计算信号
        data = self.calculate_signals(df)
        
        # 初始化
        capital = initial_capital
        position = 0  # 持仓数量
        trades = []  # 交易记录
        
        # 遍历每一天
        for i in range(len(data)):
            row = data.iloc[i]
            
            # 买入信号
            if row['signal'] == 1 and position == 0:
                # 全仓买入
                shares = int(capital / row['close'])
                cost = shares * row['close'] * (1 + commission)
                
                if cost <= capital:
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
            
            # 卖出信号
            elif row['signal'] == -1 and position > 0:
                # 全部卖出
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
        
        # 如果最后还有持仓，按最后价格卖出
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
        
        # 计算收益
        final_value = capital
        total_return = (final_value - initial_capital) / initial_capital * 100
        
        # 计算买入持有收益
        buy_hold_return = (data.iloc[-1]['close'] - data.iloc[0]['close']) / data.iloc[0]['close'] * 100
        
        # 计算最大回撤
        data['strategy_value'] = initial_capital
        current_capital = initial_capital
        current_position = 0
        
        for i in range(len(data)):
            row = data.iloc[i]
            if row['signal'] == 1 and current_position == 0:
                shares = int(current_capital / row['close'])
                current_position = shares
                current_capital -= shares * row['close'] * (1 + commission)
            elif row['signal'] == -1 and current_position > 0:
                current_capital += current_position * row['close'] * (1 - commission)
                current_position = 0
            
            # 计算当前总资产
            if current_position > 0:
                data.loc[data.index[i], 'strategy_value'] = current_capital + current_position * row['close']
            else:
                data.loc[data.index[i], 'strategy_value'] = current_capital
        
        # 最大回撤
        data['cummax'] = data['strategy_value'].cummax()
        data['drawdown'] = (data['strategy_value'] - data['cummax']) / data['cummax'] * 100
        max_drawdown = data['drawdown'].min()
        
        # 交易次数
        num_trades = len([t for t in trades if t['action'] == 'BUY'])
        
        # 胜率
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
            'data': data
        }
    
    def plot_results(self, result):
        """
        绘制回测结果
        
        Args:
            result: backtest 返回的结果
        """
        data = result['data']
        trades = result['trades']
        
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 10))
        
        # 图1: 价格和均线
        ax1.plot(data.index, data['close'], label='收盘价', linewidth=1)
        ax1.plot(data.index, data['ma_short'], label=f'MA{self.short_period}', linewidth=1)
        ax1.plot(data.index, data['ma_long'], label=f'MA{self.long_period}', linewidth=1)
        
        # 标记买卖点
        buy_signals = [t for t in trades if t['action'] == 'BUY']
        sell_signals = [t for t in trades if t['action'] == 'SELL']
        
        if buy_signals:
            buy_dates = [t['date'] for t in buy_signals]
            buy_prices = [t['price'] for t in buy_signals]
            ax1.scatter(buy_dates, buy_prices, color='red', marker='^', s=100, label='买入', zorder=5)
        
        if sell_signals:
            sell_dates = [t['date'] for t in sell_signals]
            sell_prices = [t['price'] for t in sell_signals]
            ax1.scatter(sell_dates, sell_prices, color='green', marker='v', s=100, label='卖出', zorder=5)
        
        ax1.set_title(f'{self.name} 策略回测 - 价格与信号', fontsize=14)
        ax1.set_ylabel('价格', fontsize=12)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 图2: 资产曲线
        ax2.plot(data.index, data['strategy_value'], label='策略资产', linewidth=2)
        ax2.axhline(y=result['initial_capital'], color='gray', linestyle='--', label='初始资金')
        ax2.set_title('资产曲线', fontsize=14)
        ax2.set_ylabel('资产价值', fontsize=12)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 图3: 回撤
        ax3.fill_between(data.index, 0, data['drawdown'], color='red', alpha=0.3)
        ax3.plot(data.index, data['drawdown'], color='red', linewidth=1)
        ax3.set_title(f'回撤曲线 (最大回撤: {result["max_drawdown"]:.2f}%)', fontsize=14)
        ax3.set_ylabel('回撤 (%)', fontsize=12)
        ax3.set_xlabel('日期', fontsize=12)
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('../backtest/ma_strategy_result.png', dpi=150, bbox_inches='tight')
        print("✅ 图表已保存到 backtest/ma_strategy_result.png")
        plt.show()
    
    def print_summary(self, result):
        """
        打印回测摘要
        
        Args:
            result: backtest 返回的结果
        """
        print("\n" + "="*60)
        print(f"【{self.name} 策略回测报告】")
        print("="*60)
        print(f"初始资金:     ¥{result['initial_capital']:,.2f}")
        print(f"最终资产:     ¥{result['final_value']:,.2f}")
        print(f"总收益率:     {result['total_return']:.2f}%")
        print(f"买入持有收益: {result['buy_hold_return']:.2f}%")
        print(f"最大回撤:     {result['max_drawdown']:.2f}%")
        print(f"交易次数:     {result['num_trades']}")
        print(f"胜率:         {result['win_rate']:.2f}%")
        print("="*60)
        
        # 打印前5笔交易
        if result['trades']:
            print("\n前5笔交易记录:")
            for i, trade in enumerate(result['trades'][:5]):
                print(f"{i+1}. {trade['date'].strftime('%Y-%m-%d')} | "
                      f"{trade['action']:4s} | "
                      f"价格: ¥{trade['price']:.2f} | "
                      f"数量: {trade['shares']}")


# 测试代码
if __name__ == '__main__':
    print("双均线策略测试")
    print("请先运行 data_fetcher.py 获取数据")
