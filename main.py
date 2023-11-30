from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from pymongo import MongoClient
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Use a singleton pattern for MongoDB connection
# Replace the connection string with your MongoDB Atlas connection string
# Example: "mongodb+srv://username:password@cluster0.mongodb.net/mydatabase?retryWrites=true&w=majority"
mongo_connection_string = "mongodb+srv://synisoft:s6492628827@cluster0.flvotav.mongodb.net/gst_data?retryWrites=true&w=majority"
client = MongoClient(mongo_connection_string)
db = client.get_database()
collection = db["gst_data"]

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/search/{gst_number}")
async def search_by_gst(gst_number: str):
    try:
        print(f"Searching for GST number: {gst_number}")

        # Search for the entry with the given GST number
        result = collection.find_one({"gst_number": gst_number})
        print(f"MongoDB query result: {result}")

        # If the entry is found, return company name and state
        if result:
            # Take pan number from gst, which is 10 digits, using slicing methods
            pan_number = gst_number[2:12]
            return JSONResponse(content={"gst_number": result["gst_number"], "company_name": result["company_name"], "state": result["state"], "pan_number": pan_number})
        else:
            return JSONResponse(content={"message": "GST number not found"}, status_code=404)
    except Exception as e:
        # Proper error handling
        return JSONResponse(content={"message": f"An error occurred: {str(e)}"}, status_code=500)



#TO RUN THE FASTAPI

#uvicorn main:app --reload 
