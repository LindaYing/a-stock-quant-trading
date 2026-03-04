"""
A股量化交易系统 - 主程序
学习阶段 Demo

功能:
1. 获取股票数据
2. 运行双均线策略
3. 回测并展示结果
"""

import sys
import os

# 添加路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def main():
    """主函数"""
    
    from utils.data_fetcher import DataFetcher
    from strategies.ma_strategy import MAStrategy
    
    print("=" * 60)
    print("🚀 A股量化交易系统 - 学习阶段")
    print("=" * 60)
    
    # 1. 初始化数据获取器
    print("\n【步骤1】初始化数据获取器...")
    fetcher = DataFetcher(data_dir='./data')
    
    # 2. 获取股票数据
    print("\n【步骤2】获取股票数据...")
    print("示例: 平安银行 (000001)")
    
    # 先尝试从本地加载
    df = fetcher.load_stock_data('000001')
    
    # 如果本地没有，从网络获取
    if df is None:
        print("本地无数据，正在从网络获取...")
        df = fetcher.get_stock_history('000001')
        if df is not None:
            fetcher.save_stock_data('000001', df)
    
    if df is None:
        print("❌ 无法获取数据，程序退出")
        return
    
    print(f"\n数据概览:")
    print(f"- 时间范围: {df.index[0]} 至 {df.index[-1]}")
    print(f"- 数据条数: {len(df)}")
    print(f"- 起始价格: {df.iloc[0]['close']:.2f}")
    print(f"- 最新价格: {df.iloc[-1]['close']:.2f}")
    
    # 3. 运行策略
    print("\n【步骤3】运行双均线策略...")
    strategy = MAStrategy(short_period=5, long_period=20)
    
    # 4. 回测
    print("\n【步骤4】回测策略...")
    results = strategy.backtest(df, initial_capital=100000)
    
    # 5. 展示结果
    print("\n" + "=" * 60)
    print("📊 回测结果")
    print("=" * 60)
    
    print(f"\n💰 收益情况:")
    print(f"  初始资金: ¥{results['initial_capital']:,.2f}")
    print(f"  最终资金: ¥{results['final_value']:,.2f}")
    print(f"  策略收益: {results['total_return']:.2f}%")
    print(f"  买入持有: {results['buy_hold_return']:.2f}%")
    print(f"  超额收益: {results['total_return'] - results['buy_hold_return']:.2f}%")
    
    print(f"\n📈 风险指标:")
    print(f"  最大回撤: {results['max_drawdown']:.2f}%")
    
    print(f"\n🔄 交易统计:")
    print(f"  交易次数: {results['num_trades']}")
    print(f"  胜率: {results['win_rate']:.2f}%")
    
    print(f"\n📋 最近5笔交易:")
    trades_df = results['trades_df']
    if len(trades_df) > 0:
        print(trades_df.tail(5).to_string())
    else:
        print("  无交易记录")
    
    # 6. 绘制图表
    print("\n【步骤5】生成可视化图表...")
    try:
        strategy.plot_results(results['data'], results['trades_df'])
        print("✅ 图表已生成并保存")
    except Exception as e:
        print(f"⚠️  图表生成失败: {e}")
    
    print("\n" + "=" * 60)
    print("✨ 回测完成！")
    print("=" * 60)
    
    # 7. 保存结果
    print("\n【步骤6】保存回测结果...")
    try:
        results['data'].to_csv('./data/backtest_result.csv')
        trades_df.to_csv('./data/trades.csv')
        print("✅ 结果已保存到 ./data/ 目录")
    except Exception as e:
        print(f"⚠️  保存失败: {e}")


def quick_test():
    """快速测试 - 不需要真实数据"""
    
    from strategies.ma_strategy import MAStrategy
    
    print("=" * 60)
    print("🧪 快速测试模式 (使用模拟数据)")
    print("=" * 60)
    
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    
    # 生成模拟数据
    print("\n生成模拟股票数据...")
    dates = pd.date_range(start='2021-01-01', end='2024-01-01', freq='D')
    
    # 模拟价格走势 (带趋势的随机游走)
    np.random.seed(42)
    returns = np.random.randn(len(dates)) * 0.02 + 0.0005  # 日收益率
    prices = 10 * np.exp(np.cumsum(returns))  # 价格
    
    df = pd.DataFrame({
        'open': prices * (1 + np.random.randn(len(dates)) * 0.01),
        'high': prices * (1 + abs(np.random.randn(len(dates))) * 0.02),
        'low': prices * (1 - abs(np.random.randn(len(dates))) * 0.02),
        'close': prices,
        'volume': np.random.randint(1000000, 10000000, len(dates))
    }, index=dates)
    
    print(f"✅ 生成了 {len(df)} 天的模拟数据")
    
    # 运行策略
    print("\n运行双均线策略...")
    strategy = MAStrategy(short_period=5, long_period=20)
    results = strategy.backtest(df, initial_capital=100000)
    
    # 展示结果
    print("\n" + "=" * 60)
    print("📊 回测结果 (模拟数据)")
    print("=" * 60)
    
    print(f"\n💰 收益情况:")
    print(f"  策略收益: {results['total_return']:.2f}%")
    print(f"  买入持有: {results['buy_hold_return']:.2f}%")
    
    print(f"\n📈 风险指标:")
    print(f"  最大回撤: {results['max_drawdown']:.2f}%")
    
    print(f"\n🔄 交易统计:")
    print(f"  交易次数: {results['num_trades']}")
    print(f"  胜率: {results['win_rate']:.2f}%")
    
    print("\n✨ 测试完成！")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='A股量化交易系统')
    parser.add_argument('--test', action='store_true', help='快速测试模式')
    args = parser.parse_args()
    
    if args.test:
        quick_test()
    else:
        main()
