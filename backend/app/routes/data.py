from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.services.crawler import crawlWebsiteForData
from fastapi import APIRouter
from app.dto.main import SearchRequestDTO
from app.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated
from app.services.dbFuncs import getDataFromDB, insertIntoDatabase

router = APIRouter()

dbDependency = Annotated[Session, Depends(get_db)]

@router.post("/crawl")
async def search(searchRequest: SearchRequestDTO = None, db: dbDependency = None):
    
    try:
        print("Inside the /crawl route")

        if searchRequest is None:
            return JSONResponse(content={"message": "Please provide a search term"}, status_code=400)

        print("Checking if data is already present in DB for", searchRequest.term)
        alreadyPresentData = getDataFromDB(db, searchRequest.term)

        if alreadyPresentData["status"] == True:
            print("Data already present in DB for ", searchRequest.term)
            return JSONResponse(content={"message": "Data already present in DB", "data": alreadyPresentData}, status_code=200)
        
        print("Data not present in DB, scraping the website for data")
        companyDetails = await crawlWebsiteForData(searchRequest)

        response = insertIntoDatabase(db, companyDetails)
        if response["status"] == False:
            return JSONResponse(content={"message": response["message"], "data": companyDetails}, status_code=400)

        print("Returning data from /crawl route")
        return JSONResponse(content={"message": "Data inserted successfully", "data": companyDetails}, status_code=200)
    except Exception as e:
        print("Error encountered in ./crawl route: ", e)
        return JSONResponse(content={"message": "Error encountered in /crawl route", "error": str(e)}, status_code=400)

@router.post("/find")
async def search(searchRequest: SearchRequestDTO = None, db: dbDependency = None):
    print("Inside the /find route")

    try:
        data = getDataFromDB(db, searchRequest.term)

        if data["status"] == False:
            return JSONResponse(content={"message": data["message"], "error": data["error"] if data["error"] is not None else data["message"]}, status_code=400)

        print("Returning data from /find route")
        return JSONResponse(content={"message": "Data found successfully", "data": data}, status_code=200)
    except Exception as e:
        print("Unable to process request: ", e)
        return JSONResponse(content={"message": "Error encountered in /find route", "error": str(e)}, status_code=400)