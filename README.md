# Library Management System
A Library Management System built using FastAPI, Python, SQLAlchemy, and MySQL.

# Features
- Category Management
- Book Management
- Member Management
- Borrow Record Management
- CRUD operations
- REST API endpoints
- Swagger UI for API testing

# Technologies Used
- Python
- FastAPI
- SQLAlchemy
- MySQL
- Pydantic
- Uvicorn

# How to Run
1. Create and activate a virtual environment.
2. Install the required packages:
'''bash
pip install -r requirements.txt
3. Configure the database connection in the '.env' file.
4. Start the FastAPI server:
   uvicorn app.main:app --reload
5. Open Swagger UI:
   http://127.0.0.1:8000/docs