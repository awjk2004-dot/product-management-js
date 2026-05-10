from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, database

app = FastAPI()

# ✅ تصحيح إعدادات CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",      # Live Server
        "http://localhost:5500",
        "http://127.0.0.1:3000",      # تطوير محلي آخر
        "http://localhost:3000",
        "http://127.0.0.1:8000",      # السيرفر نفسه
        "http://localhost:8000",
        "null",                        # لو فتحت الملف مباشرة file://
        "*"                            # 🔴 مؤقتاً للاختبار (بعدين شيله)
    ],
    allow_credentials=True,
    allow_methods=["*"],               # يسمح بكل الطرق (GET, POST, PUT, DELETE)
    allow_headers=["*"],               # يسمح بكل الهيدرز
)

# ... باقي الكود كما هو ...

# إنشاء الجداول
models.Base.metadata.create_all(bind=database.engine)

# دالة حساب المجموع
def calculate_total(price: float, taxes: float, ads: float, discount: float) -> float:
    return price + taxes + ads - discount

# ------------------- POST - إضافة منتج -------------------
@app.post("/products/")
def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    try:
        print(f"📦 استلام منتج: {product}")  # للتصحيح
        
        new_product = models.Product(
            title=product.title,
            price=product.price,
            taxes=product.taxes,
            ads=product.ads,
            discount=product.discount,
            category=product.category
        )
        
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        
        print(f"✅ تم الحفظ بنجاح، ID: {new_product.id}")
        return {"message": "Product created", "product": new_product}
    except Exception as e:
        print(f"❌ خطأ: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# ------------------- GET - جلب كل المنتجات -------------------
@app.get("/products/")
def get_products(db: Session = Depends(database.get_db)):
    products = db.query(models.Product).all()
    print(f"📋 عدد المنتجات في قاعدة البيانات: {len(products)}")
    
    # تحويل البيانات للواجهة مع إضافة total
    result = []
    for product in products:
        result.append({
            "id": product.id,
            "title": product.title,
            "price": product.price,
            "taxes": product.taxes,
            "ads": product.ads,
            "discount": product.discount,
            "total": calculate_total(product.price, product.taxes, product.ads, product.discount),
            "category": product.category
        })
    
    return result

# ------------------- PUT - تحديث منتج -------------------
@app.put("/products/{product_id}")
def update_product(product_id: int, updated_data: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="المنتج غير موجود")
    
    product.title = updated_data.title
    product.price = updated_data.price
    product.taxes = updated_data.taxes
    product.ads = updated_data.ads
    product.discount = updated_data.discount
    product.category = updated_data.category
    
    db.commit()
    db.refresh(product)
    
    return {
        "id": product.id,
        "title": product.title,
        "price": product.price,
        "taxes": product.taxes,
        "ads": product.ads,
        "discount": product.discount,
        "total": calculate_total(product.price, product.taxes, product.ads, product.discount),
        "category": product.category
    }

# ------------------- DELETE - حذف منتج -------------------
@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(database.get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
        return {"message": "Product deleted"}
    raise HTTPException(status_code=404, detail="المنتج غير موجود")

# ------------------- SEARCH - بحث -------------------
@app.get("/products/search/")
def search_products(title: str = None, category: str = None, db: Session = Depends(database.get_db)):
    query = db.query(models.Product)
    if title:
        query = query.filter(models.Product.title.ilike(f"%{title}%"))
    if category:
        query = query.filter(models.Product.category.ilike(f"%{category}%"))
    
    products = query.all()
    result = []
    for product in products:
        result.append({
            "id": product.id,
            "title": product.title,
            "price": product.price,
            "taxes": product.taxes,
            "ads": product.ads,
            "discount": product.discount,
            "total": calculate_total(product.price, product.taxes, product.ads, product.discount),
            "category": product.category
        })
    return result