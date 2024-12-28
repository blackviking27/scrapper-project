from app.models.company import Company


def insertIntoDatabase(db, companyDetails):
    try:
        if db is not None and companyDetails is not None:
            for data in companyDetails:
                companyData = Company(
                    name=data["name"],
                    documentNumber=data["documentNumber"],
                    status=data["status"],
                    detailsUrl=data["detailsUrl"],
                    filingInformation=data["details"]["filingInformation"],
                    principalAddress=data["details"]["principalAddress"],
                    mailingAddress=data["details"]["mailingAddress"],
                    registeredAgent=data["details"]["registeredAgent"],
                    officers=data["details"]["officers"],
                    annualReports=data["details"]["annualReports"],
                    documentImages=data["details"]["documentImages"]
                )

                db.add(companyData)
                db.commit()
                db.refresh(companyData)

            return {"status": True, "message": "Data inserted successfully"}
        else:
            return {"status": False, "message": "Database connection is not available or data is missing"}
    except Exception as e:
        print("Failed to insert data into DB: ", e)
        return {"status": False, "message": "Failed to insert data into DB " + str(e)}


def getDataFromDB(db, term):
    if term is None :
        return {"message": "Please provide a search term", "status": False}

    if db is None:
        return {"message": "Database connection is not available", "status": False}

    try:
        print("Started searching in DB for", term)
        companyDetails = db.query(Company).filter(Company.name.ilike(f"%{term}%")).all()

        results = []
        for data in companyDetails:
            results.append({
                "name": data.name,
                "documentNumber": data.documentNumber,
                "status": data.status,
                "detailsUrl": data.detailsUrl,
                "details": {
                    "filingInformation": data.filingInformation,
                    "principalAddress": data.principalAddress,
                    "mailingAddress": data.mailingAddress,
                    "registeredAgent": data.registeredAgent,
                    "officers": data.officers,
                    "annualReports": data.annualReports,
                    "documentImages": data.documentImages
                }
            })
        
        print("Search completed for", term, results)
        if len(results) == 0:
            print("Data not found for", term, results)
            return {"message": "Data not found", "status": False, "error": "No results found"}
            
        return {"message": "Data found successfully", "data": results, "status": True}
    
    except Exception as e:
        print("Unable to process request: ", e)
        return {"message": "Data not found", "error": str(e), "status": False}