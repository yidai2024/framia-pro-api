# Framia.pro API 接口分析

## 概述
Framia.pro 是一个使用 Auth0 认证系统的网站，需要登录才能访问主要功能。

## 发现的接口

### 主站接口 (framia.pro)
- `GET /create` - 创建页面（需要登录）
- `GET /auth/login` - 登录入口
- `POST /auth/callback` - OAuth回调

### 登录系统 (login.framia.pro)
- `GET /authorize` - OAuth2授权端点
- `GET /u/login/identifier` - 登录页面
- `POST /u/login/identifier` - 提交邮箱
- `GET /u/signup/identifier` - 注册页面

## 技术栈
- **认证**: Auth0 (支持PKCE)
- **验证码**: Cloudflare Turnstile
- **前端**: React

## 文件说明
- `README.md` - 本文件
- `data/` - 抓取数据
- `scripts/` - 抓取脚本

## 使用方法
```bash
cd scripts
python3 framia_capture.py
```
