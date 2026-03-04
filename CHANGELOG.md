# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- MACD 策略
- 布林带策略
- 策略参数优化工具
- 批量回测功能

---

## [1.0.0] - 2026-03-04

### Added
- 🎉 初始版本发布
- 📊 数据获取模块
  - A股股票列表获取
  - 历史行情数据（支持前复权/后复权）
  - 指数数据获取
  - 本地缓存机制
- 🎯 双均线交易策略
  - 金叉买入，死叉卖出
  - 可自定义均线周期
  - 完整信号生成逻辑
- 📈 回测引擎
  - 手续费计算
  - 资金管理
  - 性能指标（收益率、回撤、胜率等）
- 📊 可视化系统
  - K线图 + 均线
  - 买卖信号标注
  - 资金曲线
  - 回撤曲线
  - 基于 ECharts 的交互式图表
- 💻 命令行界面
  - demo.py - 快速演示
  - main.py - 完整版
- 🌐 Web 界面
  - 基于 Flask 的轻量级服务
  - 响应式设计（电脑+手机）
  - 实时参数调整
  - 数据导出功能
- 🔒 安全功能
  - 用户名密码登录
  - Session 会话管理
  - 自动超时保护
  - IP 访问控制
  - 参数验证
- 📝 完整文档
  - README.md - 项目说明
  - WEB_GUIDE.md - Web使用指南
  - SECURITY.md - 安全配置指南
  - PROJECT_SUMMARY.md - 项目总结
  - RELEASE_NOTES.md - 发布说明
  - USER_GUIDE.md - 使用指南

### Fixed
- 修复手续费计算导致资金不足的问题
- 修复 macOS 端口 5000 被占用的问题（改用 8080）

### Changed
- 从 Streamlit 切换到 Flask（安装更快）
- 优化回测性能

### Security
- 添加登录认证机制
- 添加 Session 管理
- 添加访问控制

---

## Version Naming Convention

- **Major (X.0.0)**: 重大功能更新，可能不兼容旧版本
- **Minor (1.X.0)**: 新功能添加，向后兼容
- **Patch (1.0.X)**: Bug 修复和小改进

---

## Links

- [Release Notes](RELEASE_NOTES.md)
- [User Guide](USER_GUIDE.md)
- [Security Guide](SECURITY.md)

---

*最后更新：2026年3月4日*
