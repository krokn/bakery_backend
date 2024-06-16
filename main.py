from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.product.router import router as productRouter
from src.user.router import router as userRouter
from src.order.router import router as orderRouter



app = FastAPI(
    title="Прикольный интернет магазин"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(productRouter)
app.include_router(userRouter)
app.include_router(orderRouter)



