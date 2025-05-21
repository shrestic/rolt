# 🧩 ROLT – Custom Mechanical Keyboard Platform

> **ROLT** is a full-stack platform that empowers users to build custom mechanical keyboards, manage accessories, chat with support in real-time, and complete payments via VNPAY.

🔗 **ERD Diagram**: [View here](https://dbdiagram.io/d/67ff1d279cea640381dff496)

---

## 🚀 Features

### 👤 User Authentication & Roles

* Login, register, email verification, password reset
* Role-based: **Customer**, **Support**, **Technician**, **Product Manager**, etc.

### 🧑‍💼 User & Staff Profiles

* View & update profile information

### 🛍️ Product Management (Staff Only)

* Full CRUD: `Kit`, `Switch`, `Keycap`, `Accessory`
* Manage **preset** & **custom builds**

### 🧰 Services

* Add-on services: **lubing**, **assembly**, **tuning**, etc.

### 🔧 Build System

* **Preset builds**: ready-to-order
* **Custom builds**: select parts and services

### 💳 VNPAY Integration

* Secure payments (sandbox & production-ready)
* Confirmation emails sent on successful orders

### 💬 Real-time Customer Support Chat

* Live chat: customer ↔ support/technician
* Max 2 participants/room
* Role switch: replaced staff = view-only mode

### 📦 Inventory Management

* Tracks stock for all components
* Integrated with ordering and builds

### ⚙️ Optimization

* Layer 7 anti-DDoS logic implemented
* Redis caching for heavy GET endpoints
* Layer 3 protection (WAF, firewall) in planning

### 📚 API Documentation

* Available at: `/api/docs` (in progress)

---

## 🛠 Getting Started (Dev Container)

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd rolt
```

### 2. Migrate & Seed Database

```bash
python manage.py migrate
python manage.py init_roles
```

**Mock product data:**

```bash
psql -U <your_db_user> -d <your_db_name> -f seed.sql
```

### 3. Start WebSocket Chat Locally

```bash
wscat -c "ws://www.rolt.cloud/ws/chat/support-phong-issue-001/?token=<your-token>"
```

Sample message exchange:

```json
> {"message": "Hello"}
< {"type": "chat_message", "message": "Hello", "user": "davidmiller"}
< {"message": "Connection closed due to inactivity.", "user": "system"}
```

---

## 🌐 CI/CD & Deployment Options
![rolt-ci_cd drawio](https://github.com/user-attachments/assets/c91bb72f-bfb3-4e2f-a0e3-683b346dddd4)

### ✅ Option 1: Heroku (Quick Start)

#### Step 1: Merge `.env` Files

```bash
python merge_production_dotenvs_in_dotenv.py
```

#### Step 2: Configure Heroku

* Use `.example.env` to set all required vars.
* Use [Heroku Config CLI Plugin](https://github.com/xavdid/heroku-config) for convenience.

#### Step 3: VNPAY (Optional)

* Register sandbox: search **"VNPAY đăng ký tài khoản sandbox"**
* Use [Ngrok](https://ngrok.com) to test IPN callbacks
* Configure callback here:
  👉 [VNPAY Merchant Portal](https://sandbox.vnpayment.vn/merchantv2/Users/Login.htm?ReturnUrl=%2fmerchantv2%2fAccount%2fTerminalEdit.htm)

---

### 🧱 Option 2: AWS Production via Terraform

#### 🔧 Provisioned Resources

* **ECS Fargate** (containers)
* **ALB** (load balancing)
* **RDS PostgreSQL** (database)
* **ElastiCache Redis**
* **S3** (media/static)
* **CloudWatch Logs**
* **VPC** with subnets (public/private)
* **Terraform** IaC
* **GitHub Actions** CI/CD pipeline

#### 🧩 Terraform Usage

1. Create `terraform.tfvars` or use env variables:

```hcl
region                = "ap-southeast-1"
aws_access_key_id     = "..."
aws_secret_access_key = "..."
rds_password          = "..."
django_secret_key     = "..."
vnpay_hash_secret_key = "..."
```

2. Initialize Terraform:

```bash
cd terraform/
terraform init
```

3. Plan and apply:

```bash
terraform plan -out=tfplan
terraform apply tfplan
```

🔧 Customize image/environment config via `variables.tf`.

---

## 🖼 AWS Architecture

![ROLT AWS Architecture Diagram](https://github.com/user-attachments/assets/bf180a8c-f18a-488e-9351-55f7aaff5b5a)

---

## 🧾 Notes

* All WebSocket chat messages are stored server-side
* Token-based authentication required for WebSocket
* Inventory tracking is real-time and tightly coupled with builds
* SendGrid is recommended for email delivery

---

## ✅ Project Checklist

* [x] Email confirmation & reset
* [x] VNPAY integration (sandbox)
* [x] Inventory control
* [x] Real-time customer chat
* [x] Custom & preset builds
* [x] Redis optimization

---

## 💻 Useful Commands

```bash
pytest
pre-commit run --all-files
```

---

## 📬 Contact

For questions or support:
📧 **[support@rolt.com](mailto:support@rolt.com)**

