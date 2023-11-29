from fastapi import FastAPI, Request  #to build api
from fastapi.responses import JSONResponse, HTMLResponse #to jsonsify and give html response
from pymongo import MongoClient #to connect mongodb
from fastapi.templating import Jinja2Templates #to guide the file

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/search/{gst_number}")
async def search_by_gst(gst_number: str):
    print(f"Searching for GST number: {gst_number}")


    # Connecting to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["gst_data"]
    collection = db["gst_data"]

    # Search for the entry with the given GST number
    result = collection.find_one({"gst_number": gst_number})
    print(f"MongoDB query result: {result}")


    # If the entry is found, return company name and state
    if result:

        #take pan number from gst which is 10 digits, by using slicing methods
        pan_number = gst_number[2:12]
        return JSONResponse(content={"gst_number": result["gst_number"], "company_name": result["company_name"], "state": result["state"], "pan_number": pan_number})
    else:
        return JSONResponse(content={"message": "GST number not found"}, status_code=404)


#TO RUN THE FASTAPI

#uvicorn main:app --reload 
