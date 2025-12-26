# 📁 Document Manager Backend API

A **production‑oriented backend system** built using **FastAPI**, designed to manage documents using a **hybrid database architecture (MySQL + MongoDB)** with **local file storage**.

This project demonstrates real‑world backend engineering concepts, including file handling, multi‑database integration, API design, pagination, filtering, and soft deletion.

---

## 🚀 Project Objective

To design and implement a scalable document management backend that:

- Stores actual files on disk  
- Stores structured metadata in MySQL  
- Stores flexible metadata (tags, description) in MongoDB  
- Exposes clean, reusable APIs  
- Supports searching, filtering, pagination, download, and deletion  

---

## 🧠 System Architecture

### Hybrid Storage Design

```
                      Client
                        |
                        v
                  FastAPI APIs
                        |
                        v
+----------------+-------------------+------------------+
| File System    | MySQL             | MongoDB          |
| (uploads/)     | Structured Data   | Flexible Data    |
| Actual Files   | File Metadata     | Tags & Desc      |
+----------------+-------------------+------------------+
```

### Upload Flow

1. Client uploads file + metadata  
2. File is stored on disk  
3. File metadata saved in MySQL  
4. Description & tags saved in MongoDB  
5. Both linked using `file_id`  

---

## 🛠 Tech Stack

- **Framework:** FastAPI  
- **ORM:** SQLAlchemy  
- **Databases:**  
  - MySQL (structured metadata)  
  - MongoDB (flexible metadata)  
- **Validation:** Pydantic  
- **File Storage:** Local filesystem  
- **API Documentation:** Swagger (OpenAPI)  

---

## ✨ Core Backend Features

### 📤 File Upload
- Multipart file upload  
- Disk storage for files  
- Metadata persistence in MySQL  
- Tags & description persistence in MongoDB  
- Duplicate file prevention  

### 📥 File Download
- Secure file download by `file_id`  
- Validation against deleted files  
- Disk existence check  

### 🗑 Soft Delete
- Logical deletion using `is_deleted` flag  
- Files renamed with `_deleted` suffix  
- Prevents accidental data loss  
- Deleted files excluded from normal queries  

### 🔍 Search & Filtering
- Search by file name  
- Filter by:
  - File type  
  - File size range  
  - Upload date range  
  - Tags (MongoDB)  
- SQL + MongoDB merged response  

### 📄 Pagination
- Page‑wise data retrieval  
- Efficient slicing after filtering  
- Scales for large datasets  

---

## 📡 API Endpoints Overview

### General
- `GET /docmanager/about`

### File Operations
- `POST /document/upload`
- `GET /document/download/{id}`
- `DELETE /document/delete/{id}` *(Soft delete)*

### Retrieval & Search
- `GET /document/retrival`
- `GET /document/searching_Filtering`

---

## 📂 Project Structure

```
DOCUMENT_MANAGER/
├── api/
│   └── endpoints/
│       ├── about.py
│       ├── upload.py
│       ├── download.py
│       ├── delete.py
│       ├── search.py
│       └── retrival.py
├── database/
│   ├── mysql/
│   │   ├── database.py
│   │   └── models.py
│   ├── mongodb/
│   │   └── configuration.py
│   └── schemas.py
├── frontend 
│   ├── script.js
│   ├── styles.css
├── services/
│   ├── mysql_service.py
│   ├── mongodb_service.py
│   └── file_service.py
├── uploads/
├── index.html
├── main.py
├── requirements.txt
└── README.md
```

---

## ▶️ How to Run the Backend

### 1️⃣ Clone Project
```bash
git clone <repository-url>
cd DOCUMENT_MANAGER
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Database Setup
- Create MySQL database: `document_manager`
- Configure MongoDB connection in:
  ```
  database/mongodb/configuration.py
  ```

### 5️⃣ Run Server
```bash
uvicorn main:app --reload
```

### 6️⃣ API Documentation
Open browser:
```
http://localhost:8000/docs
```

---

## 🧩 Design Decisions

- MySQL for structured relational metadata  
- MongoDB for flexible document metadata  
- Soft delete for auditability  
- Disk storage for performance and simplicity  
- Service layer for separation of concerns  
- Modular routing for maintainability  

---

## 📄 Resume‑Ready Summary

- Built APIs using FastAPI  
- Implemented file upload & download system  
- Integrated MySQL and MongoDB in one backend  
- Designed hybrid database architecture  
- Implemented pagination, search & filtering  
- Implemented soft delete mechanism  
- Built modular, scalable backend system  

---

## 👨‍💻 Author

**Sayan Sarkar**  
Backend Developer  
FastAPI • MySQL • MongoDB
