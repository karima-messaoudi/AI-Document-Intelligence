from fastapi import FastAPI
from src.api.routes.load_cv import router as load_cv_router
from src.api.routes.chat import router as chat_router
from src.api.routes.invoice import router as invoice_router 

app = FastAPI(title="CV Intelligence API")

app.include_router(load_cv_router)
app.include_router(chat_router)
app.include_router(invoice_router)  
