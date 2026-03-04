"""
A股量化交易系统 - 版本信息
"""

__version__ = "1.0.0"
__version_name__ = "Genesis"
__release_date__ = "2026-03-04"
__author__ = "Nova (星悦)"
__description__ = "A股量化交易学习系统"

def get_version_info():
    """获取版本信息"""
    return {
        'version': __version__,
        'version_name': __version_name__,
        'release_date': __release_date__,
        'author': __author__,
        'description': __description__
    }

def print_version():
    """打印版本信息"""
    print(f"A股量化交易系统 v{__version__} ({__version_name__})")
    print(f"发布日期: {__release_date__}")
    print(f"作者: {__author__}")
