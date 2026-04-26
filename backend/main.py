from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
import os
import uuid
import shutil

# ==================== CONFIGURATION ====================
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="Milk Jugs Collection API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== DATABASE MOCK (SQLite for MVP) ====================
import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db():
    conn = sqlite3.connect("collection.db")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                full_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                manufacturer TEXT,
                author_form TEXT,
                author_decoration TEXT,
                form_name TEXT,
                decoration_name TEXT,
                year_issue TEXT,
                period TEXT,
                material TEXT,
                condition TEXT,
                size TEXT,
                location TEXT,
                comment TEXT,
                is_public BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
            
            CREATE TABLE IF NOT EXISTS photos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER NOT NULL,
                file_path TEXT NOT NULL,
                is_main BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (item_id) REFERENCES items(id)
            );
            
            CREATE INDEX IF NOT EXISTS idx_items_user ON items(user_id);
            CREATE INDEX IF NOT EXISTS idx_items_public ON items(is_public);
            CREATE INDEX IF NOT EXISTS idx_photos_item ON photos(item_id);
        """)
        conn.commit()

init_db()

# ==================== SECURITY ====================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    with get_db() as conn:
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    
    if user is None:
        raise credentials_exception
    return dict(user)

# ==================== PYDANTIC MODELS ====================
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ItemCreate(BaseModel):
    manufacturer: Optional[str] = None
    author_form: Optional[str] = None
    author_decoration: Optional[str] = None
    form_name: Optional[str] = None
    decoration_name: Optional[str] = None
    year_issue: Optional[str] = None
    period: Optional[str] = None
    material: Optional[str] = None
    condition: Optional[str] = None
    size: Optional[str] = None
    location: Optional[str] = None
    comment: Optional[str] = None
    is_public: bool = False

class ItemUpdate(BaseModel):
    manufacturer: Optional[str] = None
    author_form: Optional[str] = None
    author_decoration: Optional[str] = None
    form_name: Optional[str] = None
    decoration_name: Optional[str] = None
    year_issue: Optional[str] = None
    period: Optional[str] = None
    material: Optional[str] = None
    condition: Optional[str] = None
    size: Optional[str] = None
    location: Optional[str] = None
    comment: Optional[str] = None
    is_public: Optional[bool] = None

class PhotoResponse(BaseModel):
    id: int
    item_id: int
    file_path: str
    is_main: bool

class ItemResponse(BaseModel):
    id: int
    user_id: int
    manufacturer: Optional[str]
    author_form: Optional[str]
    author_decoration: Optional[str]
    form_name: Optional[str]
    decoration_name: Optional[str]
    year_issue: Optional[str]
    period: Optional[str]
    material: Optional[str]
    condition: Optional[str]
    size: Optional[str]
    location: Optional[str]
    comment: Optional[str]
    is_public: bool
    photos: List[PhotoResponse] = []

# ==================== AUTH ROUTES ====================
@app.post("/auth/register", response_model=dict)
async def register(user: UserCreate):
    with get_db() as conn:
        existing = conn.execute("SELECT id FROM users WHERE email = ?", (user.email,)).fetchone()
        if existing:
            raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
        
        hashed_pw = get_password_hash(user.password)
        cursor = conn.execute(
            "INSERT INTO users (email, hashed_password, full_name) VALUES (?, ?, ?)",
            (user.email, hashed_pw, user.full_name)
        )
        conn.commit()
        return {"message": "Пользователь успешно зарегистрирован", "user_id": cursor.lastrowid}

@app.post("/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with get_db() as conn:
        user = conn.execute("SELECT * FROM users WHERE email = ?", (form_data.username,)).fetchone()
    
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/auth/me", response_model=dict)
async def get_me(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "full_name": current_user["full_name"],
        "created_at": current_user["created_at"]
    }

# ==================== ITEM ROUTES ====================
items_router = APIRouter(prefix="/items", tags=["items"])

@items_router.get("", response_model=List[ItemResponse])
async def get_items(
    search: Optional[str] = None,
    manufacturer: Optional[str] = None,
    author_form: Optional[str] = None,
    author_decoration: Optional[str] = None,
    form_name: Optional[str] = None,
    decoration_name: Optional[str] = None,
    period: Optional[str] = None,
    my_collection: bool = False,
    current_user: dict = Depends(get_current_user)
):
    with get_db() as conn:
        query = """
            SELECT i.*, u.email as owner_email 
            FROM items i 
            JOIN users u ON i.user_id = u.id 
            WHERE 1=1
        """
        params = []
        
        if my_collection:
            query += " AND i.user_id = ?"
            params.append(current_user["id"])
        else:
            query += " AND (i.is_public = 1 OR i.user_id = ?)"
            params.append(current_user["id"])
        
        if search:
            query += """ AND (
                i.manufacturer LIKE ? OR i.author_form LIKE ? OR 
                i.author_decoration LIKE ? OR i.form_name LIKE ? OR 
                i.decoration_name LIKE ? OR i.comment LIKE ?
            )"""
            search_pattern = f"%{search}%"
            params.extend([search_pattern] * 6)
        
        if manufacturer:
            query += " AND i.manufacturer LIKE ?"
            params.append(f"%{manufacturer}%")
        
        if author_form:
            query += " AND i.author_form LIKE ?"
            params.append(f"%{author_form}%")
        
        if author_decoration:
            query += " AND i.author_decoration LIKE ?"
            params.append(f"%{author_decoration}%")
        
        if form_name:
            query += " AND i.form_name LIKE ?"
            params.append(f"%{form_name}%")
        
        if decoration_name:
            query += " AND i.decoration_name LIKE ?"
            params.append(f"%{decoration_name}%")
        
        if period:
            query += " AND i.period LIKE ?"
            params.append(f"%{period}%")
        
        query += " ORDER BY i.created_at DESC"
        
        items = conn.execute(query, params).fetchall()
        
        result = []
        for item in items:
            photos = conn.execute(
                "SELECT * FROM photos WHERE item_id = ?", (item["id"],)
            ).fetchall()
            item_dict = dict(item)
            item_dict["photos"] = [dict(p) for p in photos]
            result.append(item_dict)
        
        return result

@items_router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, current_user: dict = Depends(get_current_user)):
    with get_db() as conn:
        item = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        
        if not item:
            raise HTTPException(status_code=404, detail="Предмет не найден")
        
        # Проверка прав доступа
        if item["user_id"] != current_user["id"] and not item["is_public"]:
            raise HTTPException(status_code=403, detail="Нет доступа к этому предмету")
        
        photos = conn.execute(
            "SELECT * FROM photos WHERE item_id = ?", (item_id,)
        ).fetchall()
        
        item_dict = dict(item)
        item_dict["photos"] = [dict(p) for p in photos]
        return item_dict

@items_router.post("", response_model=ItemResponse)
async def create_item(
    manufacturer: Optional[str] = Form(None),
    author_form: Optional[str] = Form(None),
    author_decoration: Optional[str] = Form(None),
    form_name: Optional[str] = Form(None),
    decoration_name: Optional[str] = Form(None),
    year_issue: Optional[str] = Form(None),
    period: Optional[str] = Form(None),
    material: Optional[str] = Form(None),
    condition: Optional[str] = Form(None),
    size: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    comment: Optional[str] = Form(None),
    is_public: bool = Form(False),
    photos: List[UploadFile] = File([]),
    current_user: dict = Depends(get_current_user)
):
    with get_db() as conn:
        cursor = conn.execute(
            """INSERT INTO items 
            (user_id, manufacturer, author_form, author_decoration, form_name, 
             decoration_name, year_issue, period, material, condition, size, 
             location, comment, is_public) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (current_user["id"], manufacturer, author_form, author_decoration,
             form_name, decoration_name, year_issue, period, material, condition,
             size, location, comment, is_public)
        )
        item_id = cursor.lastrowid
        
        uploaded_photos = []
        for photo in photos:
            if photo.filename:
                ext = os.path.splitext(photo.filename)[1]
                filename = f"{uuid.uuid4()}{ext}"
                filepath = os.path.join(UPLOAD_DIR, filename)
                
                with open(filepath, "wb") as buffer:
                    shutil.copyfileobj(photo.file, buffer)
                
                is_main = len(uploaded_photos) == 0
                conn.execute(
                    "INSERT INTO photos (item_id, file_path, is_main) VALUES (?, ?, ?)",
                    (item_id, filepath, is_main)
                )
                uploaded_photos.append({"file_path": filepath})
        
        conn.commit()
        
        item = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        photos_list = conn.execute(
            "SELECT * FROM photos WHERE item_id = ?", (item_id,)
        ).fetchall()
        
        item_dict = dict(item)
        item_dict["photos"] = [dict(p) for p in photos_list]
        return item_dict

@items_router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    manufacturer: Optional[str] = Form(None),
    author_form: Optional[str] = Form(None),
    author_decoration: Optional[str] = Form(None),
    form_name: Optional[str] = Form(None),
    decoration_name: Optional[str] = Form(None),
    year_issue: Optional[str] = Form(None),
    period: Optional[str] = Form(None),
    material: Optional[str] = Form(None),
    condition: Optional[str] = Form(None),
    size: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    comment: Optional[str] = Form(None),
    is_public: Optional[bool] = Form(None),
    photos: List[UploadFile] = File([]),
    current_user: dict = Depends(get_current_user)
):
    with get_db() as conn:
        item = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        
        if not item:
            raise HTTPException(status_code=404, detail="Предмет не найден")
        
        if item["user_id"] != current_user["id"]:
            raise HTTPException(status_code=403, detail="Нет прав на редактирование")
        
        updates = {}
        for field in ["manufacturer", "author_form", "author_decoration", "form_name",
                      "decoration_name", "year_issue", "period", "material", 
                      "condition", "size", "location", "comment"]:
            value = locals()[field]
            if value is not None:
                updates[field] = value
        
        if is_public is not None:
            updates["is_public"] = is_public
        
        updates["updated_at"] = datetime.utcnow().isoformat()
        
        if updates:
            set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
            values = list(updates.values()) + [item_id]
            conn.execute(f"UPDATE items SET {set_clause} WHERE id = ?", values)
        
        for photo in photos:
            if photo.filename:
                ext = os.path.splitext(photo.filename)[1]
                filename = f"{uuid.uuid4()}{ext}"
                filepath = os.path.join(UPLOAD_DIR, filename)
                
                with open(filepath, "wb") as buffer:
                    shutil.copyfileobj(photo.file, buffer)
                
                is_main = len(photos) == 1 and not any(
                    p["is_main"] for p in conn.execute(
                        "SELECT * FROM photos WHERE item_id = ?", (item_id,)
                    ).fetchall()
                )
                conn.execute(
                    "INSERT INTO photos (item_id, file_path, is_main) VALUES (?, ?, ?)",
                    (item_id, filepath, is_main)
                )
        
        conn.commit()
        
        item = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        photos_list = conn.execute(
            "SELECT * FROM photos WHERE item_id = ?", (item_id,)
        ).fetchall()
        
        item_dict = dict(item)
        item_dict["photos"] = [dict(p) for p in photos_list]
        return item_dict

@items_router.delete("/{item_id}")
async def delete_item(item_id: int, current_user: dict = Depends(get_current_user)):
    with get_db() as conn:
        item = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        
        if not item:
            raise HTTPException(status_code=404, detail="Предмет не найден")
        
        if item["user_id"] != current_user["id"]:
            raise HTTPException(status_code=403, detail="Нет прав на удаление")
        
        photos = conn.execute("SELECT * FROM photos WHERE item_id = ?", (item_id,)).fetchall()
        for photo in photos:
            if os.path.exists(photo["file_path"]):
                os.remove(photo["file_path"])
        
        conn.execute("DELETE FROM photos WHERE item_id = ?", (item_id,))
        conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()
        
        return {"message": "Предмет удален"}

@items_router.delete("/{item_id}/photos/{photo_id}")
async def delete_photo(item_id: int, photo_id: int, current_user: dict = Depends(get_current_user)):
    with get_db() as conn:
        item = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        
        if not item:
            raise HTTPException(status_code=404, detail="Предмет не найден")
        
        if item["user_id"] != current_user["id"]:
            raise HTTPException(status_code=403, detail="Нет прав на удаление фото")
        
        photo = conn.execute("SELECT * FROM photos WHERE id = ?", (photo_id,)).fetchone()
        if not photo:
            raise HTTPException(status_code=404, detail="Фото не найдено")
        
        if os.path.exists(photo["file_path"]):
            os.remove(photo["file_path"])
        
        conn.execute("DELETE FROM photos WHERE id = ?", (photo_id,))
        conn.commit()
        
        return {"message": "Фото удалено"}

app.include_router(items_router)

# ==================== PUBLIC ROUTES ====================
@app.get("/")
async def root():
    return {"message": "API для коллекции фарфоровых молочников", "version": "1.0.0"}

@app.get("/public/items", response_model=List[ItemResponse])
async def get_public_items(
    search: Optional[str] = None,
    manufacturer: Optional[str] = None,
    author_form: Optional[str] = None,
    author_decoration: Optional[str] = None,
    form_name: Optional[str] = None,
    decoration_name: Optional[str] = None,
    period: Optional[str] = None
):
    with get_db() as conn:
        query = """
            SELECT i.*, u.email as owner_email 
            FROM items i 
            JOIN users u ON i.user_id = u.id 
            WHERE i.is_public = 1
        """
        params = []
        
        if search:
            query += """ AND (
                i.manufacturer LIKE ? OR i.author_form LIKE ? OR 
                i.author_decoration LIKE ? OR i.form_name LIKE ? OR 
                i.decoration_name LIKE ? OR i.comment LIKE ?
            )"""
            search_pattern = f"%{search}%"
            params.extend([search_pattern] * 6)
        
        if manufacturer:
            query += " AND i.manufacturer LIKE ?"
            params.append(f"%{manufacturer}%")
        
        if author_form:
            query += " AND i.author_form LIKE ?"
            params.append(f"%{author_form}%")
        
        if author_decoration:
            query += " AND i.author_decoration LIKE ?"
            params.append(f"%{author_decoration}%")
        
        if form_name:
            query += " AND i.form_name LIKE ?"
            params.append(f"%{form_name}%")
        
        if decoration_name:
            query += " AND i.decoration_name LIKE ?"
            params.append(f"%{decoration_name}%")
        
        if period:
            query += " AND i.period LIKE ?"
            params.append(f"%{period}%")
        
        query += " ORDER BY i.created_at DESC"
        
        items = conn.execute(query, params).fetchall()
        
        result = []
        for item in items:
            photos = conn.execute(
                "SELECT * FROM photos WHERE item_id = ?", (item["id"],)
            ).fetchall()
            item_dict = dict(item)
            item_dict["photos"] = [dict(p) for p in photos]
            result.append(item_dict)
        
        return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
