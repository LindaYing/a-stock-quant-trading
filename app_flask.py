"""
轻量级 Web 界面 - 使用 Flask
不需要 Streamlit，安装更快
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import json
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from strategies.simple_ma_strategy import SimpleMAStrategy

app = Flask(__name__)


def generate_mock_data(days=500, start_price=10, volatility=0.02, trend=0.0005):
    """生成模拟数据"""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    np.random.seed(42)
    returns = np.random.randn(days) * volatility + trend
    prices = start_price * np.exp(np.cumsum(returns))
    
    df = pd.DataFrame({
        'open': prices * (1 + np.random.randn(days) * 0.01),
        'high': prices * (1 + abs(np.random.randn(days)) * 0.02),
        'low': prices * (1 - abs(np.random.randn(days)) * 0.02),
        'close': prices,
        'volume': np.random.randint(1000000, 10000000, days)
    }, index=dates)
    
    return df


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/backtest', methods=['POST'])
def backtest():
    """回测接口"""
    try:
        data = request.json
        
        # 获取参数
        short_period = int(data.get('short_period', 5))
        long_period = int(data.get('long_period', 20))
        initial_capital = float(data.get('initial_capital', 100000))
        days = int(data.get('days', 500))
        volatility = float(data.get('volatility', 0.02))
        trend = float(data.get('trend', 0.0005))
        
        # 生成数据
        df = generate_mock_data(days, volatility=volatility, trend=trend)
        
        # 运行策略
        strategy = SimpleMAStrategy(short_period=short_period, long_period=long_period)
        results = strategy.backtest(df, initial_capital=initial_capital)
        
        # 准备返回数据
        data_with_signals = results['data']
        
        # K线数据
        kline_data = []
        for idx, row in data_with_signals.iterrows():
            kline_data.append({
                'date': idx.strftime('%Y-%m-%d'),
                'open': float(row['open']),
                'high': float(row['high']),
                'low': float(row['low']),
                'close': float(row['close']),
                'volume': int(row['volume']),
                'ma_short': float(row['ma_short']) if not pd.isna(row['ma_short']) else None,
                'ma_long': float(row['ma_long']) if not pd.isna(row['ma_long']) else None,
                'strategy_value': float(row['strategy_value']) if 'strategy_value' in row else None
            })
        
        # 交易记录
        trades = []
        for trade in results['trades']:
            trades.append({
                'date': trade['date'].strftime('%Y-%m-%d'),
                'action': trade['action'],
                'price': float(trade['price']),
                'shares': int(trade['shares'])
            })
        
        # 返回结果
        return jsonify({
            'success': True,
            'metrics': {
                'initial_capital': results['initial_capital'],
                'final_value': float(results['final_value']),
                'total_return': float(results['total_return']),
                'buy_hold_return': float(results['buy_hold_return']),
                'max_drawdown': float(results['max_drawdown']),
                'num_trades': results['num_trades'],
                'win_rate': float(results['win_rate'])
            },
            'kline_data': kline_data,
            'trades': trades
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 A股量化交易系统 - Web界面")
    print("=" * 60)
    print("\n📱 访问地址:")
    print("   本地: http://localhost:8080")
    print("   网络: http://0.0.0.0:8080")
    print("\n💡 提示: 按 Ctrl+C 停止服务\n")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=8080, debug=False)
