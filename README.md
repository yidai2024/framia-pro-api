# Framia.pro API 接口分析报告

## 抓取时间
2026-04-16

## 目标
https://framia.pro/create

## 发现的所有接口

### 1. 主站接口 (framia.pro)
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /create | 创建页面（需要登录） |
| GET | /auth/login | 登录入口 |
| POST | /auth/callback | OAuth回调（从authorize参数中发现） |

### 2. 登录系统接口 (login.framia.pro)
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /authorize | OAuth2授权端点 |
| GET | /u/login/identifier | 登录页面（输入邮箱） |
| POST | /u/login/identifier | 提交邮箱 |
| GET | /u/login/password | 密码输入页面（推测） |
| POST | /u/login/password | 提交密码（推测） |
| GET | /u/signup/identifier | 注册页面 |

### 3. OAuth2授权参数解析
```
授权URL: https://login.framia.pro/authorize
参数:
- audience: https://framia.pro
- scope: openid profile email offline_access
- client_id: WUwcEbgDTyRAWZFIIALMujp1VDss4wQW
- redirect_uri: https://framia.pro/auth/callback
- response_type: code
- code_challenge: jE__6raNgu5ng1QP6oYlMHlPywSo4O-ULu5U_d6pG7M
- code_challenge_method: S256 (PKCE)
- state: fVUyk-o3cv38b42xIbcvXEC1t-ONlSLZ00sWtoeLkMo
- nonce: KrdH4kK3UMNFz8V09q_0GoZzN1buc4MrgxnSSC5NT68
```

### 4. 登录表单字段
```
表单1（主登录表单）:
- state (hidden) - Auth0状态参数
- username (email) - 邮箱地址
- captcha (hidden) - 验证码
- js-available (hidden)
- webauthn-available (hidden)
- is-brave (hidden)
- webauthn-platform-available (hidden)

表单2（Google OAuth）:
- state (hidden)
- connection (hidden) - 值为 google-oauth2
```

### 5. 验证码系统
| 域名 | 说明 |
|------|------|
| challenges.cloudflare.com | Cloudflare Turnstile验证码 |
| www.recaptcha.net | Google reCAPTCHA |
| js.hcaptcha.com | hCaptcha |
| status.arkoselabs.com | Arkose Labs状态检查 |

### 6. CDN资源
| 域名 | 路径 | 说明 |
|------|------|------|
| cdn.auth0.com | /ulp/react-components/1.186.0/css/main_wcag_compliant.cdn.min.css | Auth0登录UI样式 |
| assets-cdn.framia.pro | /home/favicon.svg | 网站图标 |
| assets-cdn.framia.pro | /home/login-background.png | 登录背景图 |

## 认证流程
1. 访问 `/create` → 重定向到 `/auth/login`
2. `/auth/login` → 重定向到 `login.framia.pro/authorize`
3. `authorize` → 重定向到 `/u/login/identifier`（输入邮箱）
4. 提交邮箱 → 跳转到 `/u/login/password`（输入密码）
5. 提交密码 → 验证码验证
6. 验证成功 → 回调到 `/auth/callback?code=xxx`
7. 使用code换取access_token
8. 使用access_token访问API

## 技术栈
- **认证**: Auth0 (支持PKCE)
- **验证码**: Cloudflare Turnstile, reCAPTCHA, hCaptcha
- **前端**: React (Auth0 ULP)
- **CDN**: Cloudflare

## 下一步
需要登录凭据才能继续抓取/create页面的API接口

## 文件位置
- 所有请求: /root/framia_all_requests.json
- API请求: /root/framia_api_requests.json
- 页面HTML: /root/framia_step1.html
- 截图: /opt/crawler-tools/data/framia_step1.png (在服务器上)
