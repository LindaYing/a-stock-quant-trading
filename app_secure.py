"""
安全增强版 Web 界面
添加了访问控制和安全措施
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from version import __version__, __version_name__, __release_date__
from functools import wraps
import pandas as pd
import numpy as np
import json
from datetime import datetime
import sys
import os
import secrets

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from strategies.simple_ma_strategy import SimpleMAStrategy

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # 随机密钥

# 配置
CONFIG = {
    'username': 'admin',  # 默认用户名
    'password': 'PASS_WORD',  # 密码已修改
    'allow_localhost_only': False,  # True = 仅允许本机访问
    'session_timeout': 3600  # 会话超时时间（秒）
}


def require_auth(f):
    """登录验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return jsonify({'success': False, 'error': '未登录'}), 401
        return f(*args, **kwargs)
    return decorated_function


def check_ip_allowed():
    """检查 IP 是否允许访问"""
    if CONFIG['allow_localhost_only']:
        client_ip = request.remote_addr
        if client_ip not in ['127.0.0.1', 'localhost', '::1']:
            return False
    return True


@app.before_request
def before_request():
    """请求前检查"""
    if not check_ip_allowed():
        return jsonify({'error': '访问被拒绝'}), 403


@app.route('/')
def index():
    """主页"""
    if not session.get('logged_in'):
        return render_template('login.html')
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    """登录"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if username == CONFIG['username'] and password == CONFIG['password']:
        session['logged_in'] = True
        session.permanent = True
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': '用户名或密码错误'}), 401


@app.route('/logout')
def logout():
    """登出"""
    session.pop('logged_in', None)
    return redirect(url_for('index'))


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


@app.route('/api/backtest', methods=['POST'])
@require_auth
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
        
        # 参数验证
        if short_period >= long_period:
            return jsonify({'success': False, 'error': '短期均线必须小于长期均线'})
        if days > 2000:
            return jsonify({'success': False, 'error': '数据天数不能超过2000天'})
        
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
    print(f"🔒 A股量化交易系统 v{__version__} ({__version_name__})")
    print("=" * 60)
    print("\n🔐 安全设置:")
    print(f"   用户名: {CONFIG['username']}")
    print(f"   密码: {CONFIG['password']}")
    print(f"   仅本机访问: {'是' if CONFIG['allow_localhost_only'] else '否'}")
    print("\n📱 访问地址:")
    if CONFIG['allow_localhost_only']:
        print("   本地: http://localhost:8080")
        print("   ⚠️  已启用本机访问限制")
    else:
        print("   本地: http://localhost:8080")
        print("   网络: http://0.0.0.0:8080")
        print("   ⚠️  网络访问已开启，请确保在安全网络环境")
    print("\n💡 提示:")
    print("   - 首次登录后请修改密码")
    print("   - 按 Ctrl+C 停止服务")
    print("   - 修改配置请编辑 app_secure.py 中的 CONFIG")
    print(f"\n📅 发布日期: {__release_date__}")
    print("\n" + "=" * 60 + "\n")
    
    app.run(host='0.0.0.0', port=8080, debug=False)
