"""
A股量化交易系统 - Web界面
基于 Streamlit 构建，支持电脑和手机浏览
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from strategies.simple_ma_strategy import SimpleMAStrategy

# 页面配置
st.set_page_config(
    page_title="A股量化交易系统",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
        padding: 10px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #FF6B6B;
    }
    h1 {
        color: #FF4B4B;
    }
    .success-box {
        padding: 20px;
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        border-radius: 5px;
        margin: 10px 0;
    }
    .warning-box {
        padding: 20px;
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


def generate_mock_data(days=500, start_price=10, volatility=0.02, trend=0.0005):
    """生成模拟股票数据"""
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


def plot_candlestick_with_ma(data, trades_df=None):
    """绘制K线图和均线"""
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.7, 0.3],
        subplot_titles=('价格走势', '成交量')
    )
    
    # K线图
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data['open'],
            high=data['high'],
            low=data['low'],
            close=data['close'],
            name='K线',
            increasing_line_color='#FF4B4B',
            decreasing_line_color='#00CC96'
        ),
        row=1, col=1
    )
    
    # 短期均线
    if 'ma_short' in data.columns:
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['ma_short'],
                name='短期均线',
                line=dict(color='#FFA500', width=2)
            ),
            row=1, col=1
        )
    
    # 长期均线
    if 'ma_long' in data.columns:
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['ma_long'],
                name='长期均线',
                line=dict(color='#1E90FF', width=2)
            ),
            row=1, col=1
        )
    
    # 买卖信号
    if trades_df is not None and len(trades_df) > 0:
        buy_trades = trades_df[trades_df['action'] == 'BUY']
        sell_trades = trades_df[trades_df['action'] == 'SELL']
        
        if len(buy_trades) > 0:
            fig.add_trace(
                go.Scatter(
                    x=buy_trades['date'],
                    y=buy_trades['price'],
                    mode='markers',
                    name='买入',
                    marker=dict(
                        symbol='triangle-up',
                        size=15,
                        color='red',
                        line=dict(color='darkred', width=2)
                    )
                ),
                row=1, col=1
            )
        
        if len(sell_trades) > 0:
            fig.add_trace(
                go.Scatter(
                    x=sell_trades['date'],
                    y=sell_trades['price'],
                    mode='markers',
                    name='卖出',
                    marker=dict(
                        symbol='triangle-down',
                        size=15,
                        color='green',
                        line=dict(color='darkgreen', width=2)
                    )
                ),
                row=1, col=1
            )
    
    # 成交量
    colors = ['red' if row['close'] >= row['open'] else 'green' 
              for _, row in data.iterrows()]
    
    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data['volume'],
            name='成交量',
            marker_color=colors,
            showlegend=False
        ),
        row=2, col=1
    )
    
    # 布局
    fig.update_layout(
        title='股票走势与交易信号',
        xaxis_rangeslider_visible=False,
        height=700,
        hovermode='x unified',
        template='plotly_white'
    )
    
    fig.update_xaxes(title_text="日期", row=2, col=1)
    fig.update_yaxes(title_text="价格 (¥)", row=1, col=1)
    fig.update_yaxes(title_text="成交量", row=2, col=1)
    
    return fig


def plot_equity_curve(data):
    """绘制资金曲线"""
    fig = go.Figure()
    
    # 策略资金曲线
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['strategy_value'],
            name='策略资金',
            line=dict(color='#FF4B4B', width=2),
            fill='tonexty'
        )
    )
    
    # 买入持有基准
    initial_value = data['strategy_value'].iloc[0]
    buy_hold_value = initial_value * (data['close'] / data['close'].iloc[0])
    
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=buy_hold_value,
            name='买入持有',
            line=dict(color='#00CC96', width=2, dash='dash')
        )
    )
    
    fig.update_layout(
        title='资金曲线对比',
        xaxis_title='日期',
        yaxis_title='资金 (¥)',
        height=400,
        hovermode='x unified',
        template='plotly_white'
    )
    
    return fig


def plot_drawdown(data):
    """绘制回撤曲线"""
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['drawdown'],
            name='回撤',
            fill='tozeroy',
            line=dict(color='#FF4B4B', width=2)
        )
    )
    
    fig.update_layout(
        title='回撤曲线',
        xaxis_title='日期',
        yaxis_title='回撤 (%)',
        height=300,
        hovermode='x unified',
        template='plotly_white'
    )
    
    return fig


def main():
    # 标题
    st.title("📈 A股量化交易系统")
    st.markdown("---")
    
    # 侧边栏 - 参数配置
    with st.sidebar:
        st.header("⚙️ 策略配置")
        
        # 数据源选择
        data_source = st.radio(
            "数据源",
            ["模拟数据", "真实数据（需安装akshare）"],
            help="模拟数据用于快速测试，真实数据需要安装akshare库"
        )
        
        st.markdown("---")
        
        # 策略参数
        st.subheader("双均线策略参数")
        
        short_period = st.slider(
            "短期均线周期",
            min_value=3,
            max_value=30,
            value=5,
            step=1,
            help="短期移动平均线的天数"
        )
        
        long_period = st.slider(
            "长期均线周期",
            min_value=10,
            max_value=120,
            value=20,
            step=5,
            help="长期移动平均线的天数"
        )
        
        st.markdown("---")
        
        # 回测参数
        st.subheader("回测参数")
        
        initial_capital = st.number_input(
            "初始资金 (¥)",
            min_value=10000,
            max_value=10000000,
            value=100000,
            step=10000
        )
        
        commission = st.number_input(
            "手续费率 (%)",
            min_value=0.01,
            max_value=1.0,
            value=0.03,
            step=0.01,
            format="%.2f"
        ) / 100
        
        if data_source == "模拟数据":
            st.markdown("---")
            st.subheader("模拟数据参数")
            
            days = st.slider("数据天数", 100, 1000, 500, 50)
            volatility = st.slider("波动率", 0.01, 0.05, 0.02, 0.01)
            trend = st.slider("趋势", -0.001, 0.002, 0.0005, 0.0001, format="%.4f")
        
        st.markdown("---")
        
        # 运行按钮
        run_backtest = st.button("🚀 开始回测", use_container_width=True)
    
    # 主界面
    if run_backtest:
        with st.spinner('正在运行回测...'):
            try:
                # 获取数据
                if data_source == "模拟数据":
                    df = generate_mock_data(days=days, volatility=volatility, trend=trend)
                    st.info(f"📊 使用模拟数据: {len(df)} 天")
                else:
                    try:
                        from utils.data_fetcher import DataFetcher
                        fetcher = DataFetcher()
                        df = fetcher.get_stock_history('000001')  # 平安银行
                        if df is None:
                            st.error("无法获取真实数据，请确保已安装 akshare")
                            return
                        st.success(f"📊 获取真实数据: 平安银行 (000001), {len(df)} 天")
                    except Exception as e:
                        st.error(f"获取数据失败: {e}")
                        return
                
                # 创建策略
                strategy = SimpleMAStrategy(short_period=short_period, long_period=long_period)
                
                # 回测
                results = strategy.backtest(df, initial_capital=initial_capital, commission=commission)
                
                # 显示结果
                st.markdown('<div class="success-box">✅ 回测完成！</div>', unsafe_allow_html=True)
                
                # 关键指标
                st.header("📊 关键指标")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "策略收益",
                        f"{results['total_return']:.2f}%",
                        delta=f"{results['total_return'] - results['buy_hold_return']:.2f}% vs 买入持有"
                    )
                
                with col2:
                    st.metric(
                        "最终资金",
                        f"¥{results['final_value']:,.0f}",
                        delta=f"¥{results['final_value'] - initial_capital:,.0f}"
                    )
                
                with col3:
                    st.metric(
                        "最大回撤",
                        f"{results['max_drawdown']:.2f}%"
                    )
                
                with col4:
                    st.metric(
                        "交易次数",
                        f"{results['num_trades']}",
                        delta=f"胜率 {results['win_rate']:.1f}%"
                    )
                
                st.markdown("---")
                
                # 图表展示
                tab1, tab2, tab3, tab4 = st.tabs(["📈 K线与信号", "💰 资金曲线", "📉 回撤分析", "📋 交易记录"])
                
                with tab1:
                    fig1 = plot_candlestick_with_ma(results['data'], results['trades_df'])
                    st.plotly_chart(fig1, use_container_width=True)
                
                with tab2:
                    fig2 = plot_equity_curve(results['data'])
                    st.plotly_chart(fig2, use_container_width=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("买入持有收益", f"{results['buy_hold_return']:.2f}%")
                    with col2:
                        excess_return = results['total_return'] - results['buy_hold_return']
                        st.metric("超额收益", f"{excess_return:.2f}%")
                
                with tab3:
                    fig3 = plot_drawdown(results['data'])
                    st.plotly_chart(fig3, use_container_width=True)
                
                with tab4:
                    if len(results['trades_df']) > 0:
                        st.dataframe(
                            results['trades_df'].style.format({
                                'price': '¥{:.2f}',
                                'cost': '¥{:.2f}',
                                'revenue': '¥{:.2f}',
                                'capital': '¥{:.2f}'
                            }),
                            use_container_width=True
                        )
                        
                        # 下载按钮
                        csv = results['trades_df'].to_csv(index=False).encode('utf-8-sig')
                        st.download_button(
                            label="📥 下载交易记录",
                            data=csv,
                            file_name=f"trades_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                    else:
                        st.warning("本次回测没有产生交易")
                
            except Exception as e:
                st.error(f"回测失败: {str(e)}")
                st.exception(e)
    
    else:
        # 欢迎页面
        st.info("👈 请在左侧配置策略参数，然后点击「开始回测」按钮")
        
        st.markdown("""
        ### 📚 使用说明
        
        1. **选择数据源**
           - 模拟数据：快速测试，无需安装额外库
           - 真实数据：需要安装 akshare (`pip install akshare`)
        
        2. **配置策略参数**
           - 短期均线：通常 5-10 天
           - 长期均线：通常 20-60 天
        
        3. **设置回测参数**
           - 初始资金：建议 10万 起步
           - 手续费率：一般 0.03%
        
        4. **查看结果**
           - K线图：查看买卖信号
           - 资金曲线：对比策略表现
           - 回撤分析：评估风险
           - 交易记录：详细交易明细
        
        ### ⚠️ 风险提示
        
        - 历史回测不代表未来收益
        - 本系统仅供学习使用
        - 实盘交易需谨慎
        """)


if __name__ == '__main__':
    main()
