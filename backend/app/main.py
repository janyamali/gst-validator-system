from fastapi import FastAPI

from app.api.routes.upload import router as upload_router
from app.api.routes.export import router as export_router
from app.api.routes.invoices import router as invoices_router

from app.core.database import engine
from app.core.database import Base

from app.models.invoice import Invoice
from app.models.validation import Validation
from app.models.claim import Claim

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(upload_router)
app.include_router(export_router)
app.include_router(invoices_router)

@app.get("/")
def home():

    return {
        "message": "GST Validator Running"
    }