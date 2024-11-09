# from fastapi import FastAPI
# import requests

# app = fastapi.FastAPI()

# #merchant service port 8001
# @app.get("/merchant/{merchant_id}")
# async def get_merchant(merchant_id: int):
#     response = requests.get(f"http://localhost:8001/merchant/{merchant_id}")
#     return response.json()

# #buyer service port 8002
# @app.get("/buyer/{buyer_id}")
# async def get_buyer(buyer_id: int):
#     response = requests.get(f"http://localhost:8002/buyer/{buyer_id}")
#     return response.json()


# #inventory service port 8003
# @app.get("/product/{product_id}")
# async def get_product(product_id: int):
#     response = requests.get(f"http://localhost:8003/product/{product_id}")
#     return response.json()

# @app.get("/product/{product_id}/stock") #uppseld
# async def get_product_stock(product_id: int):
#     response = requests.get(f"http://localhost:8003/product/{product_id}/stock")
#     return response.json()

