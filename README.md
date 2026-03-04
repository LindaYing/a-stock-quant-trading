# A股量化交易系统 - 学习阶段

一个简单易用的 A 股量化交易学习系统，适合量化交易初学者。

## 📁 项目结构

```
quant_system/
├── main.py                 # 主程序
├── requirements.txt        # 依赖包
├── data/                   # 数据目录
├── strategies/             # 策略目录
│   └── ma_strategy.py     # 双均线策略
├── utils/                  # 工具目录
│   └── data_fetcher.py    # 数据获取工具
└── backtest/              # 回测结果目录
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip3 install akshare pandas numpy matplotlib
```

### 2. 快速测试（使用模拟数据）

```bash
python3 main.py --test
```

### 3. 真实数据回测

```bash
python3 main.py
```

## 📊 功能特性

### ✅ 已实现

- **数据获取**
  - 使用 AkShare 获取免费 A 股数据
  - 支持股票列表、历史行情、指数数据
  - 本地缓存机制

- **双均线策略**
  - 经典的金叉死叉策略
  - 可自定义短期/长期均线周期
  - 完整的买卖信号生成

- **回测系统**
  - 计算策略收益率
  - 对比买入持有收益
  - 最大回撤分析
  - 交易记录统计
  - 胜率计算

- **可视化**
  - K线图 + 均线
  - 买卖信号标注
  - 资金曲线
  - 回撤曲线

### 🔜 待实现

- 更多策略（MACD、布林带、网格交易）
- 多因子选股
- 风险管理模块
- 实时监控面板
- 模拟盘交易

## 📖 使用示例

### 获取股票数据

```python
from utils.data_fetcher import DataFetcher

# 创建数据获取器
fetcher = DataFetcher(data_dir='./data')

# 获取平安银行历史数据
df = fetcher.get_stock_history('000001')

# 保存到本地
fetcher.save_stock_data('000001', df)
```

### 运行策略回测

```python
from strategies.ma_strategy import MAStrategy

# 创建策略（5日均线 vs 20日均线）
strategy = MAStrategy(short_period=5, long_period=20)

# 回测
results = strategy.backtest(df, initial_capital=100000)

# 查看结果
print(f"策略收益: {results['total_return']:.2f}%")
print(f"最大回撤: {results['max_drawdown']:.2f}%")
```

## 🎯 策略说明

### 双均线策略 (MA Strategy)

**原理：**
- 短期均线上穿长期均线 → 买入信号（金叉）
- 短期均线下穿长期均线 → 卖出信号（死叉）

**参数：**
- `short_period`: 短期均线周期，默认 5 天
- `long_period`: 长期均线周期，默认 20 天

**适用场景：**
- 趋势明显的市场
- 中长期持有

**局限性：**
- 震荡市容易频繁交易
- 存在滞后性
- 需要结合其他指标优化

## 📈 回测结果示例

```
📊 回测结果
============================================================

💰 收益情况:
  初始资金: ¥100,000.00
  最终资金: ¥125,680.50
  策略收益: 25.68%
  买入持有: 18.32%
  超额收益: 7.36%

📈 风险指标:
  最大回撤: -12.45%

🔄 交易统计:
  交易次数: 15
  胜率: 60.00%
```

## ⚠️ 风险提示

1. **本系统仅供学习使用**，不构成投资建议
2. **历史回测不代表未来收益**
3. **实盘交易需谨慎**，建议先用模拟盘测试
4. **做好风险控制**，不要投入超过承受能力的资金

## 🛠️ 技术栈

- **Python 3.9+**
- **AkShare** - 免费数据源
- **Pandas** - 数据处理
- **NumPy** - 数值计算
- **Matplotlib** - 数据可视化

## 📚 学习资源

- [AkShare 文档](https://akshare.akfamily.xyz/)
- [量化交易入门](https://www.joinquant.com/help/api/help)
- [Backtrader 文档](https://www.backtrader.com/docu/)

## 🤝 贡献

欢迎提出建议和改进！

## 📝 更新日志

### v0.1.0 (2026-03-04)
- ✅ 初始版本
- ✅ 数据获取功能
- ✅ 双均线策略
- ✅ 基础回测系统
- ✅ 可视化图表

## 📧 联系方式

如有问题，欢迎交流！

---

**免责声明：** 本项目仅用于学习和研究目的，不构成任何投资建议。投资有风险，入市需谨慎。
