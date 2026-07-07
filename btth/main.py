from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel

app = FastAPI()

DATABASE_URL = "mysql+pymysql://root:WXvs6026%40@localhost:3306/ecommerce_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ShipmentModel(Base):
    __tablename__ = "shipments"
    id = Column(Integer, primary_key=True)
    tracking_number = Column(String(50), unique=True, nullable=False)
    status = Column(String(50), default="PREPARING")

# Hàm Dependency cung cấp Database Session cho API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class CreateShipment(BaseModel):
    id: int
    tracking_number: str
    status: str

# Hàm Dependency cung cấp Database Session cho API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/shipments")
def create_shipment(tracking_number: str, db: Session = Depends(get_db)):
    try:
        check_exist = db.query(ShipmentModel).filter(tracking_number == ShipmentModel.tracking_number).first()

        if check_exist:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Mã vận đơn này đã được khởi tạo trước đó")
        
        new_shipment = ShipmentModel(tracking_number=tracking_number)
        db.add(new_shipment)
        db.commit()
        db.refresh(new_shipment)
        return new_shipment
    
    except HTTPException:
        raise
    
    except Exception as e:
        db.rollback()
        return {"message": str(e)}
    
@app.get("/shipments")
def get_shipments(db: Session = Depends(get_db)):
    shipments = db.query(ShipmentModel).all()
    return shipments