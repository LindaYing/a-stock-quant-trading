"""
快速演示 - 使用模拟数据测试策略
不需要安装 akshare 和 matplotlib
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from strategies.simple_ma_strategy import SimpleMAStrategy


def generate_mock_data(days=1000, start_price=10):
    """生成模拟股票数据"""
    dates = pd.date_range(start='2021-01-01', periods=days, freq='D')
    
    # 模拟价格走势
    np.random.seed(42)
    returns = np.random.randn(days) * 0.02 + 0.0005
    prices = start_price * np.exp(np.cumsum(returns))
    
    df = pd.DataFrame({
        'open': prices * (1 + np.random.randn(days) * 0.01),
        'high': prices * (1 + abs(np.random.randn(days)) * 0.02),
        'low': prices * (1 - abs(np.random.randn(days)) * 0.02),
        'close': prices,
        'volume': np.random.randint(1000000, 10000000, days)
    }, index=dates)
    
    return df


def main():
    print("=" * 70)
    print("🚀 A股量化交易系统 - 快速演示")
    print("=" * 70)
    
    # 生成模拟数据
    print("\n【步骤1】生成模拟股票数据...")
    df = generate_mock_data(days=1000, start_price=10)
    print(f"✅ 生成了 {len(df)} 天的数据")
    print(f"   时间范围: {df.index[0].date()} 至 {df.index[-1].date()}")
    print(f"   起始价格: ¥{df.iloc[0]['close']:.2f}")
    print(f"   最新价格: ¥{df.iloc[-1]['close']:.2f}")
    
    # 创建策略
    print("\n【步骤2】创建双均线策略...")
    strategy = SimpleMAStrategy(short_period=5, long_period=20)
    print(f"✅ 策略: {strategy.name}")
    print(f"   短期均线: {strategy.short_period} 天")
    print(f"   长期均线: {strategy.long_period} 天")
    
    # 回测
    print("\n【步骤3】运行回测...")
    results = strategy.backtest(df, initial_capital=100000)
    print("✅ 回测完成")
    
    # 展示结果
    print("\n" + "=" * 70)
    print("📊 回测结果")
    print("=" * 70)
    
    print(f"\n💰 收益情况:")
    print(f"   初始资金: ¥{results['initial_capital']:,.2f}")
    print(f"   最终资金: ¥{results['final_value']:,.2f}")
    print(f"   策略收益: {results['total_return']:.2f}%")
    print(f"   买入持有: {results['buy_hold_return']:.2f}%")
    
    if results['total_return'] > results['buy_hold_return']:
        print(f"   ✅ 超额收益: +{results['total_return'] - results['buy_hold_return']:.2f}%")
    else:
        print(f"   ❌ 跑输大盘: {results['total_return'] - results['buy_hold_return']:.2f}%")
    
    print(f"\n📈 风险指标:")
    print(f"   最大回撤: {results['max_drawdown']:.2f}%")
    
    print(f"\n🔄 交易统计:")
    print(f"   交易次数: {results['num_trades']}")
    print(f"   胜率: {results['win_rate']:.2f}%")
    
    # 显示交易记录
    if len(results['trades']) > 0:
        print(f"\n📋 交易记录 (最近10笔):")
        trades_df = results['trades_df']
        print(trades_df.tail(10).to_string(index=False))
    
    # 保存结果
    print("\n【步骤4】保存结果...")
    try:
        os.makedirs('./data', exist_ok=True)
        results['data'].to_csv('./data/demo_backtest.csv')
        results['trades_df'].to_csv('./data/demo_trades.csv')
        print("✅ 结果已保存到 ./data/ 目录")
    except Exception as e:
        print(f"⚠️  保存失败: {e}")
    
    print("\n" + "=" * 70)
    print("✨ 演示完成！")
    print("=" * 70)
    
    print("\n💡 下一步:")
    print("   1. 安装 akshare: pip3 install akshare")
    print("   2. 使用真实数据: python3 main.py")
    print("   3. 尝试不同参数: 修改 short_period 和 long_period")
    print("   4. 开发新策略: 在 strategies/ 目录添加新文件")


if __name__ == '__main__':
    main()
