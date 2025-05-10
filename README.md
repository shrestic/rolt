
# ROLT - Custom Mechanical Keyboard Platform

ROLT is a full-stack platform that allows customers to build their own custom mechanical keyboards and accessories. It supports real-time customer support chat, payment integration via VNPAY, role-based user management, inventory tracking, and customizable builds.

## 🚀 Features

- **User Authentication**
  - Login / Register
  - Email verification, password reset, account confirmation
  - Role-based access: Customer / Staff

- **User & Staff Profiles**
  - Customers and staff can update their personal information.

- **Product Management**
  - CRUD for: `Kit`, `Switch`, `Keycap`, `Accessory` (Staff only)
  - Support for both preset and custom builds

- **Service Management**
  - Services related to keyboard building (e.g., lubing, assembly, tuning)

- **Build System**
  - Preset builds (pre-designed)
  - Custom builds (customer-selected components)

- **VNPAY Integration**
  - Secure payment gateway
  - Pending & successful order confirmation emails sent to customers

- **Real-time Customer Chat**
  - Live chat between customers and support/technical staff
  - Only 2 participants per room at a time
  - Supports role-switching and viewing-only mode for replaced staff

- **Inventory System**
  - Tracks stock for each component
  - Integrated into the order & build systems

- **Performance & Optimization**
  - Optimization against DDoS/spam is currently implemented at the **application layer** (Layer 7 of OSI model).
  - Network layer** (Layer 3) protections are being planned (e.g., firewall, reverse proxy-level rules).
  - Redis caching for high-demand endpoints

- **Best Practices**
  - Built with [HackSoft Django Styleguide](https://github.com/HackSoftware/Django-Styleguide)
  - Project scaffolded via Cookiecutter Django

- **API Documentation**
  - Available at: `/api/docs` (in progress)

---

## 🛠️ Getting Started

### 1. Clone & Open in VSCode Dev Container

```bash
git clone <your-repo-url>
cd rolt
```

- Server Django sẽ tự động được khởi chạy bên trong container

### 2. Migrate & Seed Database

Mở terminal trong Dev Container và chạy:

```bash
python manage.py migrate
python manage.py init_roles
```

Manually execute SQL to mock product data:

```bash
psql -U <your_db_user> -d <your_db_name> -f seed.sql
```

### 3. Start WebSocket Chat Locally (with token)

```bash
wscat -c "ws://www.rolt.cloud/ws/chat/support-phong-issue-001/?token=<your-token>"
```

Example:
```json
> {"message":"Hello"}
< {"type": "chat_message", "message": "Hello", "user": "davidmiller"}
< {"message": "Connection closed due to inactivity.", "user": "system"}
```

---

## 🚀 Deployment (Heroku)

### 1. Merge Env Files

Run script to merge production `.env` values:

```bash
python merge_production_dotenvs_in_dotenv.py
```

### 2. Set Config on Heroku

Check the `.example.env` file for all required environment variables.
You can copy it or use it as a reference when setting Heroku config variables.


### 3. VNPAY Integration
To get started, you need a test account.
Search **"VNPAY đăng ký tài khoản sandbox"** on Google to find the official sandbox registration page.
- VNPAY is running in **sandbox mode** but enabled in production for now.
- Mock frontend using [Ngrok](https://ngrok.com/) to allow callback testing.
- Real production access requires official registration with VNPAY.
- For proper IPN (Instant Payment Notification) setup, refer to the VNPAY setup guide.
- After setting up the account, visit the following link to configure your IPN URL:
👉 https://sandbox.vnpayment.vn/merchantv2/Users/Login.htm?ReturnUrl=%2fmerchantv2%2fAccount%2fTerminalEdit.htm


---

## 📦 Notes

- All real-time chats are saved on the backend regardless of session logout.
- Token-based WebSocket authentication is enabled.
- Inventory and stock control are tied to each build item.
- Do not forget to configure SendGrid for email sending if Mailgun is removed.

---

## ✅ Checklist

- [x] Email confirmation & password reset
- [x] VNPAY Sandbox setup
- [x] Inventory tracking
- [x] WebSocket customer chat
- [x] Custom & preset builds
- [x] Redis & throttling optimization

---

## 📎 Useful Commands

```bash
pytest
pre-commit run --all-files
```
---

## 🔗 Contact

For support or questions, contact: [support@rolt.com](mailto:support@rolt.com)
