"""
A股数据获取工具
使用 AkShare 获取免费的股票数据
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import os


class DataFetcher:
    """数据获取类"""
    
    def __init__(self, data_dir='./data'):
        """
        初始化数据获取器
        
        Args:
            data_dir: 数据存储目录
        """
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def get_stock_list(self):
        """
        获取A股股票列表
        
        Returns:
            DataFrame: 股票列表
        """
        try:
            # 获取沪深A股列表
            stock_list = ak.stock_zh_a_spot_em()
            print(f"✅ 成功获取 {len(stock_list)} 只股票")
            return stock_list
        except Exception as e:
            print(f"❌ 获取股票列表失败: {e}")
            return None
    
    def get_stock_history(self, symbol, start_date=None, end_date=None, adjust='qfq'):
        """
        获取股票历史数据
        
        Args:
            symbol: 股票代码，如 '000001'
            start_date: 开始日期，格式 'YYYYMMDD'
            end_date: 结束日期，格式 'YYYYMMDD'
            adjust: 复权类型 'qfq'前复权 'hfq'后复权 ''不复权
        
        Returns:
            DataFrame: 历史数据
        """
        try:
            # 默认获取最近3年数据
            if not end_date:
                end_date = datetime.now().strftime('%Y%m%d')
            if not start_date:
                start_date = (datetime.now() - timedelta(days=365*3)).strftime('%Y%m%d')
            
            # 获取历史数据
            df = ak.stock_zh_a_hist(
                symbol=symbol,
                period="daily",
                start_date=start_date,
                end_date=end_date,
                adjust=adjust
            )
            
            if df is not None and len(df) > 0:
                # 重命名列为英文
                df.rename(columns={
                    '日期': 'date',
                    '开盘': 'open',
                    '收盘': 'close',
                    '最高': 'high',
                    '最低': 'low',
                    '成交量': 'volume',
                    '成交额': 'amount',
                    '振幅': 'amplitude',
                    '涨跌幅': 'pct_change',
                    '涨跌额': 'change',
                    '换手率': 'turnover'
                }, inplace=True)
                
                # 设置日期为索引
                df['date'] = pd.to_datetime(df['date'])
                df.set_index('date', inplace=True)
                
                print(f"✅ 成功获取 {symbol} 的 {len(df)} 条数据")
                return df
            else:
                print(f"⚠️  {symbol} 没有数据")
                return None
                
        except Exception as e:
            print(f"❌ 获取 {symbol} 数据失败: {e}")
            return None
    
    def save_stock_data(self, symbol, df):
        """
        保存股票数据到本地
        
        Args:
            symbol: 股票代码
            df: 数据DataFrame
        """
        try:
            file_path = os.path.join(self.data_dir, f'{symbol}.csv')
            df.to_csv(file_path)
            print(f"✅ 数据已保存到 {file_path}")
        except Exception as e:
            print(f"❌ 保存数据失败: {e}")
    
    def load_stock_data(self, symbol):
        """
        从本地加载股票数据
        
        Args:
            symbol: 股票代码
        
        Returns:
            DataFrame: 股票数据
        """
        try:
            file_path = os.path.join(self.data_dir, f'{symbol}.csv')
            if os.path.exists(file_path):
                df = pd.read_csv(file_path, index_col='date', parse_dates=True)
                print(f"✅ 从本地加载 {symbol} 的 {len(df)} 条数据")
                return df
            else:
                print(f"⚠️  本地没有 {symbol} 的数据")
                return None
        except Exception as e:
            print(f"❌ 加载数据失败: {e}")
            return None
    
    def get_index_history(self, index_code='000001', start_date=None, end_date=None):
        """
        获取指数历史数据
        
        Args:
            index_code: 指数代码
                '000001': 上证指数
                '399001': 深证成指
                '399006': 创业板指
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            DataFrame: 指数数据
        """
        try:
            if not end_date:
                end_date = datetime.now().strftime('%Y%m%d')
            if not start_date:
                start_date = (datetime.now() - timedelta(days=365*3)).strftime('%Y%m%d')
            
            df = ak.stock_zh_index_daily(symbol=f"sh{index_code}")
            
            if df is not None and len(df) > 0:
                df.rename(columns={
                    'date': 'date',
                    'open': 'open',
                    'close': 'close',
                    'high': 'high',
                    'low': 'low',
                    'volume': 'volume'
                }, inplace=True)
                
                df['date'] = pd.to_datetime(df['date'])
                df.set_index('date', inplace=True)
                
                # 筛选日期范围
                df = df[(df.index >= start_date) & (df.index <= end_date)]
                
                print(f"✅ 成功获取指数 {index_code} 的 {len(df)} 条数据")
                return df
            else:
                print(f"⚠️  指数 {index_code} 没有数据")
                return None
                
        except Exception as e:
            print(f"❌ 获取指数数据失败: {e}")
            return None


# 测试代码
if __name__ == '__main__':
    print("=" * 50)
    print("A股数据获取工具测试")
    print("=" * 50)
    
    # 创建数据获取器
    fetcher = DataFetcher(data_dir='../data')
    
    # 测试1: 获取股票列表
    print("\n【测试1】获取股票列表...")
    stock_list = fetcher.get_stock_list()
    if stock_list is not None:
        print(f"前5只股票:\n{stock_list.head()}")
    
    # 测试2: 获取平安银行历史数据
    print("\n【测试2】获取平安银行(000001)历史数据...")
    df = fetcher.get_stock_history('000001')
    if df is not None:
        print(f"数据预览:\n{df.head()}")
        print(f"\n数据统计:\n{df.describe()}")
        
        # 保存数据
        fetcher.save_stock_data('000001', df)
    
    # 测试3: 从本地加载数据
    print("\n【测试3】从本地加载数据...")
    df_local = fetcher.load_stock_data('000001')
    
    # 测试4: 获取上证指数
    print("\n【测试4】获取上证指数...")
    index_df = fetcher.get_index_history('000001')
    if index_df is not None:
        print(f"指数数据预览:\n{index_df.head()}")
    
    print("\n" + "=" * 50)
    print("测试完成！")
    print("=" * 50)
