
# ROLT - Custom Mechanical Keyboard Platform

ROLT is a full-stack platform that allows customers to build their own custom mechanical keyboards and accessories. It supports real-time customer support chat, payment integration via VNPAY, role-based user management, inventory tracking, and customizable builds.

# ERD Diagram
Link to the [ERD Diagram](https://dbdiagram.io/d/67ff1d279cea640381dff496)

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

## 🚀 Deployment Options

This project supports two primary deployment methods:

### ✅ Option 1: Quick Deployment via Heroku

#### Step 1: Merge Production `.env` Files

Use the following script to merge all required `.env` variables into one file:

```bash
python merge_production_dotenvs_in_dotenv.py
```

This will create a unified `.env` file for production use.

---

#### Step 2: Set Config Vars on Heroku

Check the `.example.env` file to view all required environment variables. You can:

* Set them manually via Heroku Dashboard, or
* Use the [Heroku Config CLI Plugin](https://github.com/xavdid/heroku-config) for bulk upload.

---

#### Step 3: VNPAY Integration (Optional)

If you're using VNPAY for payments:

* The integration runs in **sandbox mode** but is **production-ready**.
* Register a sandbox account at the official site by searching:
  👉 **"VNPAY đăng ký tài khoản sandbox"**
* Use [Ngrok](https://ngrok.com/) to test IPN callbacks locally.
* Configure the IPN URL after login here:
  👉 [https://sandbox.vnpayment.vn/merchantv2/Users/Login.htm?ReturnUrl=%2fmerchantv2%2fAccount%2fTerminalEdit.htm](https://sandbox.vnpayment.vn/merchantv2/Users/Login.htm?ReturnUrl=%2fmerchantv2%2fAccount%2fTerminalEdit.htm)
* Real production integration requires official merchant approval from VNPAY.

---

### 🧱 Option 2: Production Deployment via AWS & Terraform

This project includes full Infrastructure as Code (IaC) support using **Terraform** to provision and deploy on AWS.

#### 🔧 Infrastructure Components:

* **ECS Fargate** for container orchestration
* **ALB (Application Load Balancer)** for traffic routing
* **RDS (PostgreSQL)** for managed relational database
* **Elasticache (Redis)** for caching and Celery task queues
* **S3** for static/media file storage
* **CloudWatch Logs** for centralized log management
* **VPC with public/private subnets** for secure networking
* **Terraform** for provisioning
* **GitHub Actions** for CI/CD deployment automation

#### 🧩 Terraform Setup

1. Create your Terraform secrets in `terraform.tfvars` or use environment variables:

```hcl
region               = "ap-southeast-1"
aws_access_key_id    = "..."
aws_secret_access_key = "..."
rds_password         = "..."
django_secret_key    = "..."
vnpay_hash_secret_key = "..."
```

2. Initialize Terraform:

```bash
cd terraform/
terraform init
```

3. Validate and apply infrastructure:

```bash
terraform plan -out=tfplan
terraform apply tfplan
```

> You can customize environment variables and image URLs in `variables.tf`.

---

ROLT AWS Architecture Diagram
![ROLT AWS Architecture Diagram](https://github.com/user-attachments/assets/bf180a8c-f18a-488e-9351-55f7aaff5b5a)

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
