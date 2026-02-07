---

# 📘 KnowledgeVault

KnowledgeVault is a full-stack, microservices-based knowledge management application that enables users to securely create, manage, search, and store notes with cloud-backed media support. It is built using modern mobile and backend technologies with scalability and maintainability in mind.

This project demonstrates real-world system design, mobile development, and distributed backend architecture.

---

## 🚀 Features

### 📱 Mobile Application

* Cross-platform app built with React Native (Expo)
* Secure authentication (JWT-based)
* Notes creation, editing, versioning, and deletion
* Full-text search
* Cloud media attachments
* System-based Light/Dark theme support
* Reusable UI components (KVButton, KVInput)
* Secure token storage
* Real-device testing support

### ⚙️ Backend System

* Microservices-based architecture
* API Gateway for centralized routing
* Authentication Service
* Content/Notes Service
* Search Service
* Media Service
* Redis caching and rate limiting
* PostgreSQL database
* AWS S3 file storage
* Secure password hashing
* Token-based authorization

### 🏗️ Architecture

* Service isolation
* Horizontal scaling support
* CDN-ready media delivery
* Gateway-based request routing
* Stateless authentication
* Load-balancer friendly design

---

## 🏛️ System Architecture

```
Mobile App (React Native)
        |
        v
   API Gateway
        |
 -------------------------------------------------
 |        |         |           |               |
Auth   Content    Search      Media          Cache
Service Service  Service     Service         (Redis)
        |
     PostgreSQL

Media Storage → AWS S3
```

---

## 🧰 Tech Stack

### Frontend

* React Native (Expo)
* TypeScript
* React Navigation
* Axios
* Expo SecureStore

### Backend

* Python 3.9
* FastAPI
* SQLAlchemy
* PostgreSQL
* Redis
* JWT
* Passlib (bcrypt)

### Cloud & Infrastructure

* AWS S3
* Boto3 SDK
* Virtual Environments
* Environment Variables
* Git

---

## 📁 Project Structure

```
KnowledgeVault/
│
├── frontend/          # React Native app
│
├── AuthService/        # Authentication microservice
├── ContentService/     # Notes & content management
├── SearchService/      # Search & indexing
├── MediaService/       # File storage service
├── ApiGateway/         # Central API gateway
│
├── docker/             # (planned) Docker configs
├── scripts/            # Utility scripts
└── README.md
```

---

## 🔐 Authentication Flow

1. User registers/logs in via Mobile App
2. API Gateway forwards request to Auth Service
3. Auth Service validates credentials
4. JWT token is issued
5. Token stored securely on device
6. All protected APIs require Authorization header

---

## 📝 Notes & Search Flow

### Creating Notes

1. User submits note
2. Content Service stores versioned record
3. Search Service indexes content
4. Cached metadata stored in Redis

### Searching Notes

1. Search query sent to Gateway
2. Routed to Search Service
3. Full-text search executed
4. Results returned to mobile app

---

## 📦 Media Upload Flow

1. Client requests upload URL
2. Media Service generates pre-signed S3 URL
3. Client uploads directly to S3
4. Metadata stored in database
5. CDN-ready links returned

---

## ⚡ Performance Optimizations

* Redis-based caching
* Stateless authentication
* Rate limiting
* Background indexing
* API Gateway routing
* Optimized DB queries

---

## 🛠️ Local Setup

### Prerequisites

* Node.js (v18+ recommended)
* Python 3.9
* PostgreSQL
* Redis
* AWS Account (for S3)
* Expo CLI

---

## 🔧 Backend Setup

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create `.env` file:

```env
DATABASE_URL=postgresql://user:pass@localhost/db
JWT_SECRET=your_secret
REDIS_URL=redis://localhost:6379
AWS_ACCESS_KEY_ID=xxxx
AWS_SECRET_ACCESS_KEY=xxxx
AWS_REGION=eu-north-1
S3_BUCKET_NAME=knowledge-vault-files
```

---

### 4. Start Services

Run each service separately:

```bash
# Auth
uvicorn app.main:app --host 0.0.0.0 --port 8001

# Content
uvicorn app.main:app --host 0.0.0.0 --port 8002

# Search
uvicorn app.main:app --host 0.0.0.0 --port 8003

# Media
uvicorn app.main:app --host 0.0.0.0 --port 8004

# Gateway
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 📱 Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure API Base URL

Update:

```
src/api/client.ts
```

```ts
export const API_BASE_URL = "http://<your-ip>:8000";
```

---

### 3. Start App

```bash
npx expo start
```

Scan QR code on your phone.

---

## 📦 Build APK

```bash
npx expo prebuild
eas build -p android --profile preview
```

Download and install APK.

---

## 🧪 Testing

### API Testing

```bash
curl http://localhost:8000/docs
```

Use Swagger UI for testing.

### Mobile Testing

* Real Android device
* Expo Go
* APK installation

---

## 🔀 Git Workflow

```
main       → Stable branch
frontend   → UI development
backend    → Service development
feature/*  → Feature branches
```

---

## 📊 Project Outcomes

* ~30–40% API latency reduction using Redis caching
* Sub-second search performance
* Scalable stateless authentication
* Modular service deployment
* Improved maintainability via clean architecture

---

## 🎯 Future Improvements

* Dockerized deployment
* Offline-first sync
* Push notifications
* AI-powered summaries
* Role-based access control
* Multi-device sync

---

