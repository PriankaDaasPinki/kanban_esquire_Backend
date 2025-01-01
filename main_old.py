import asyncpg
import bcrypt
import secrets
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Depends, Request, UploadFile, File, Form
from pydantic import BaseModel, Field, EmailStr
from fastapi.responses import JSONResponse
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


DATABASE_URL = "postgresql://postgres:admin@localhost:5432/kanban_esquire"
SECRET_KEY = "your-secret-key"  # Replace with a secure secret key
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30


# Database mock-up (replace with actual DB logic)
class Database:
    async def acquire(self):
        # Simulate database connection
        class MockConnection:
            async def execute(self, query: str, *args):
                print(f"Executing query: {query} with args: {args}")

            async def fetchrow(self, query: str, *args):
                print(f"Fetching row with query: {query} and args: {args}")
                return (
                    {"username": "existing_user"} if "existing_user" in args else None
                )

        return MockConnection()


app.state.db = Database()


class LoginRequest(BaseModel):
    username: str
    password: str


# Pydantic model for input validation
class User(BaseModel):
    username: str = Field(..., max_length=50)
    name: str
    phone: str = Field(..., pattern=r"^\+?\d{7,15}$")  # Validates phone format
    email: EmailStr
    password: str = Field(..., min_length=8)
    designation: Optional[str] = None
    image: Optional[UploadFile] = File(None)


class PartialUserUpdate(BaseModel):
    name: Optional[str] = (Form(None),)
    phone: Optional[str] = Field(
        None, pattern=r"^\+?\d{7,15}$"
    )  # Optional phone format
    email: Optional[EmailStr] = (Form(None),)
    designation: Optional[str] = (Form(None),)
    image: Optional[UploadFile] = File(None)


# Directory to store uploaded files
UPLOAD_DIR = './uploads'
# UPLOAD_DIR.mkdir(exist_ok=True)


@app.on_event("startup")
async def startup():
    try:
        app.state.db = await asyncpg.create_pool(DATABASE_URL)
        print("Database connection successful!")
    except Exception as e:
        print(f"Error: {e}")


@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()


# Hash password
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


# Verify password
def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


# Generate JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Routes for authentication
# 74c9a2cfd13c397637d1453c1db120593623afe9 belal user finance auth token 29 dec 2024
# 74c9a2cfd13c397637d1453c1db120593623afe9
# 74c9a2cfd13c397637d1453c1db120593623afe9 belal user finance auth token 30 dec 2024 9.50 am
# d8d4083e3da421f14fddac3b377d7abda81a3c09 belal user finance auth token 30 dec 2024
# @app.post("/register/")
# async def register_user(
#     username: str,
#     name: str,
#     phone: str,
#     email: str,
#     password: str,
#     designation: str = None,
#     image: str = None,
# ):
#     hashed_password = hash_password(password)
#     async with app.state.db.acquire() as conn:
#         try:
#             await conn.execute(
#                 "INSERT INTO users (username, full_name, phone, email, password_hash, designation, user_image) VALUES ($1, $2, $3, $4, $5, $6, $7)",
#                 username,
#                 name,
#                 phone,
#                 email,
#                 hashed_password,
#                 designation,
#                 image,
#             )
#             return {"message": "User registered successfully!"}
#         except Exception as e:
#             raise HTTPException(status_code=400, detail=str(e))


@app.on_event("startup")
async def startup():
    try:
        app.state.db = await asyncpg.create_pool(DATABASE_URL)
        print("Database connection successful!")
    except Exception as e:
        print(f"Error: {e}")


@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()


# Handle file uploads asynchronously
async def save_file(file: UploadFile) -> str:
    if file:
        file_path = UPLOAD_DIR / file.filename
        async with file_path.open("wb") as f:
            content = await file.read()
            await f.write(content)
        return str(file_path)
    return None


@app.post("/register/")
async def register_user(user: User):
    hashed_password = hash_password(user.password)
    image_path = await save_file(user.image)
    async with app.state.db.acquire() as conn:
        try:
            # Check if user already exists
            existing_user = await conn.fetchrow(
                "SELECT username FROM users WHERE username = $1 OR email = $2",
                user.username,
                user.email,
            )
            if existing_user:
                raise HTTPException(status_code=400, detail="User already exists.")

            await conn.execute(
                """
                INSERT INTO users (username, full_name, phone, email, password_hash, designation, user_image) 
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                """,
                user.username,
                user.name,
                user.phone,
                user.email,
                hashed_password,
                user.designation,
                image_path,
            )
            return {"message": "User registered successfully!"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))


# @app.patch("/update-user/{username}")
# async def update_user(username: str, user_update: PartialUserUpdate):
#     async with app.state.db.acquire() as conn:
#         try:
#             # Check if user exists
#             existing_user = await conn.fetchrow(
#                 "SELECT username FROM users WHERE username = $1",
#                 username,
#             )
#             if not existing_user:
#                 raise HTTPException(status_code=404, detail="User not found.")

#             # Dynamic field updates
#             update_fields = []
#             update_values = [username]
#             index = 2

#             if user_update.name:
#                 update_fields.append(f"full_name = ${index}")
#                 update_values.append(user_update.name)
#                 index += 1
#             if user_update.phone:
#                 update_fields.append(f"phone = ${index}")
#                 update_values.append(user_update.phone)
#                 index += 1
#             if user_update.email:
#                 update_fields.append(f"email = ${index}")
#                 update_values.append(user_update.email)
#                 index += 1
#             if user_update.designation:
#                 update_fields.append(f"designation = ${index}")
#                 update_values.append(user_update.designation)
#                 index += 1
#             if user_update.image:
#                 file_path = await save_file(user_update.image)
#                 update_fields.append(f"user_image = ${index}")
#                 update_values.append(file_path)

#             if not update_fields:
#                 raise HTTPException(
#                     status_code=400, detail="No valid fields provided for update."
#                 )

#             update_query = f"""
#                 UPDATE users 
#                 SET {', '.join(update_fields)} 
#                 WHERE username = $1
#             """
#             await conn.execute(update_query, *update_values)
#             return {"message": "User updated successfully!"}
#         except Exception as e:
#             raise HTTPException(status_code=400, detail=str(e))



from pathlib import Path
from fastapi import HTTPException, UploadFile

async def save_file(upload_file: UploadFile) -> str:
    # Directory to save the uploaded files
    upload_dir = Path("uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)  # Ensure directory exists

    # Define the file path
    file_path = upload_dir / upload_file.filename

    try:
        # Open the file in binary write mode
        with open(file_path, "wb") as buffer:
            while chunk := await upload_file.read(1024):  # Read in chunks
                buffer.write(chunk)  # Write binary data directly
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    return str(file_path)


@app.patch("/update-user/{username}")
async def update_user(username: str, user_update: PartialUserUpdate):
    async with app.state.db.acquire() as conn:
        try:
            # Check if user exists
            existing_user = await conn.fetchrow(
                "SELECT username FROM users WHERE username = $1",
                username,
            )
            if not existing_user:
                raise HTTPException(status_code=404, detail="User not found.")

            # Dynamic field updates
            update_fields = []
            update_values = [username]
            index = 2

            if user_update.name:
                update_fields.append(f"full_name = ${index}")
                update_values.append(user_update.name)
                index += 1
            if user_update.phone:
                update_fields.append(f"phone = ${index}")
                update_values.append(user_update.phone)
                index += 1
            if user_update.email:
                update_fields.append(f"email = ${index}")
                update_values.append(user_update.email)
                index += 1
            if user_update.designation:
                update_fields.append(f"designation = ${index}")
                update_values.append(user_update.designation)
                index += 1
            if user_update.image:
                # Save the image file and get its path
                file_path = await save_file(user_update.image)
                update_fields.append(f"user_image = ${index}")
                update_values.append(file_path)
                index += 1

            if not update_fields:
                raise HTTPException(
                    status_code=400, detail="No valid fields provided for update."
                )

            update_query = f"""
                UPDATE users 
                SET {', '.join(update_fields)} 
                WHERE username = $1
            """
            await conn.execute(update_query, *update_values)
            return {"message": "User updated successfully!"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))




@app.post("/login/")
async def login_user(request: LoginRequest):
    username = request.username
    password = request.password
    async with app.state.db.acquire() as conn:
        print("username, password")
        print(username, password)
        user = await conn.fetchrow("SELECT * FROM users WHERE username = $1", username)
        if user and verify_password(password, user["password_hash"]):
            # Generate a session token
            session_token = secrets.token_hex(32)
            await conn.execute(
                "INSERT INTO sessions (user_id, session_token) VALUES ($1, $2)",
                user["user_id"],
                session_token,
            )

            # Generate a JWT token
            access_token = create_access_token({"sub": user["user_id"]})
            print(user)

            return {
                "message": "Login successful!",
                "session_token": session_token,
                "access_token": access_token,
                "user": user,
            }
        raise HTTPException(status_code=401, detail="Invalid username or password.")


@app.get("/protected/")
async def protected_route(request: Request):
    # Get session token from request headers
    session_token = request.headers.get("Session-Token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Session token missing.")

    # Validate session token
    async with app.state.db.acquire() as conn:
        session = await conn.fetchrow(
            "SELECT * FROM sessions WHERE session_token = $1", session_token
        )
        if not session:
            raise HTTPException(status_code=401, detail="Invalid session token.")

    return {"message": "Access granted!", "user_id": session["user_id"]}


@app.get("/token-protected/")
async def token_protected_route(request: Request):
    # Get JWT token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token missing or invalid.")

    token = auth_header.split(" ")[1]

    # Decode and validate JWT token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload.")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token invalid or expired.")

    return {"message": "Access granted!", "user_id": user_id}


@app.get("/logout/")
async def logout_user(request: Request):
    session_token = request.headers.get("Session-Token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Session token missing.")

    async with app.state.db.acquire() as conn:
        await conn.execute(
            "DELETE FROM sessions WHERE session_token = $1", session_token
        )

    return {"message": "Logged out successfully!"}
