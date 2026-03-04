# 安全配置指南

## 🔒 安全功能

### 1. 登录认证
- ✅ 用户名密码验证
- ✅ Session 会话管理
- ✅ 自动超时登出

### 2. 访问控制
- ✅ IP 白名单（可选）
- ✅ 仅本机访问模式
- ✅ API 接口保护

### 3. 数据安全
- ✅ 参数验证
- ✅ 错误处理
- ✅ 无敏感数据存储

---

## 🚀 使用安全版

### 启动安全版服务器
```bash
cd ~/.openclaw/workspace/quant_system
python3 app_secure.py
```

### 默认登录信息
- **用户名**: `admin`
- **密码**: `quant2026`

⚠️ **首次登录后请立即修改密码！**

---

## 🔧 安全配置

编辑 `app_secure.py` 中的 `CONFIG` 部分：

```python
CONFIG = {
    'username': 'admin',              # 修改用户名
    'password': 'your_password',      # 修改密码
    'allow_localhost_only': False,    # True = 仅本机访问
    'session_timeout': 3600           # 会话超时（秒）
}
```

### 配置选项说明

#### 1. 修改用户名和密码
```python
'username': 'your_username',
'password': 'your_strong_password'
```

**密码建议：**
- 至少 12 位
- 包含大小写字母、数字、特殊字符
- 不要使用常见密码

#### 2. 仅本机访问模式
```python
'allow_localhost_only': True
```

**启用后：**
- ✅ 只能从本机访问（127.0.0.1）
- ❌ 局域网其他设备无法访问
- ✅ 最安全的模式

**适用场景：**
- 只在自己电脑上使用
- 不需要手机访问
- 最高安全要求

#### 3. 会话超时
```python
'session_timeout': 3600  # 1小时
```

超时后需要重新登录。

---

## 🛡️ 安全建议

### 基础安全

1. **修改默认密码**
   - 首次启动后立即修改
   - 定期更换密码

2. **使用强密码**
   - 不要使用生日、电话等
   - 使用密码管理器

3. **限制访问**
   - 如果只自己用，开启 `allow_localhost_only`
   - 不要在公共 WiFi 使用

### 网络安全

4. **WiFi 安全**
   - 使用 WPA3 加密
   - 设置强 WiFi 密码
   - 定期更换 WiFi 密码
   - 关闭 WPS 功能

5. **防火墙**
   - 启用 macOS 防火墙
   - 只允许必要的端口

6. **VPN（可选）**
   - 在外网访问时使用 VPN
   - 推荐 WireGuard 或 Tailscale

### 高级安全

7. **HTTPS（生产环境）**
   如果需要在公网使用，配置 HTTPS：
   ```bash
   # 使用 nginx 反向代理
   # 配置 SSL 证书
   ```

8. **IP 白名单**
   只允许特定 IP 访问：
   ```python
   ALLOWED_IPS = ['192.168.1.100', '192.168.1.101']
   
   @app.before_request
   def check_ip():
       if request.remote_addr not in ALLOWED_IPS:
           return jsonify({'error': '访问被拒绝'}), 403
   ```

9. **限流保护**
   防止暴力破解：
   ```bash
   pip3 install flask-limiter
   ```

---

## 🔍 安全检查清单

### 启动前
- [ ] 已修改默认密码
- [ ] 确认访问模式（本机 or 局域网）
- [ ] WiFi 密码足够强
- [ ] 防火墙已启用

### 使用中
- [ ] 不在公共场所使用
- [ ] 不分享登录信息
- [ ] 定期检查登录日志
- [ ] 及时登出

### 停止使用
- [ ] 关闭服务器（Ctrl+C）
- [ ] 清除浏览器缓存
- [ ] 退出登录

---

## 🚨 风险说明

### 当前版本的局限性

1. **开发服务器**
   - 使用 Flask 开发服务器
   - 不适合生产环境
   - 仅供学习和个人使用

2. **无 HTTPS**
   - 数据未加密传输
   - 不要在公网使用
   - 仅限局域网

3. **简单认证**
   - 单用户模式
   - 无多因素认证
   - 无登录日志

### 不要做的事

❌ **不要在公网暴露**
- 不要配置端口转发
- 不要使用公网 IP 访问
- 不要在云服务器上运行（除非配置 HTTPS）

❌ **不要存储敏感数据**
- 不要保存真实交易账号
- 不要保存银行卡信息
- 不要保存身份证号

❌ **不要在不安全的网络使用**
- 不要在公共 WiFi 使用
- 不要在咖啡厅等场所使用
- 不要在公司网络使用（可能违反政策）

---

## 🔐 推荐配置

### 场景1：仅自己使用（最安全）
```python
CONFIG = {
    'username': 'your_username',
    'password': 'your_strong_password',
    'allow_localhost_only': True,  # 仅本机
    'session_timeout': 1800  # 30分钟
}
```

### 场景2：家庭局域网使用
```python
CONFIG = {
    'username': 'your_username',
    'password': 'your_strong_password',
    'allow_localhost_only': False,  # 允许局域网
    'session_timeout': 3600  # 1小时
}
```

**额外措施：**
- 确保 WiFi 密码强度
- 定期检查连接设备
- 使用 MAC 地址过滤

---

## 📞 遇到问题？

### 忘记密码
编辑 `app_secure.py`，修改 `CONFIG['password']`

### 无法访问
1. 检查防火墙设置
2. 确认 IP 限制配置
3. 查看服务器日志

### 被锁定
重启服务器即可

---

## 📚 进一步学习

- [OWASP Web 安全](https://owasp.org/)
- [Flask 安全最佳实践](https://flask.palletsprojects.com/en/2.3.x/security/)
- [网络安全基础](https://www.cybrary.it/)

---

**记住：安全是一个持续的过程，不是一次性的设置。保持警惕，定期检查！** 🔒
