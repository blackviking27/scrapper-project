from app.dto.main import SearchRequestDTO
import requests
from bs4 import BeautifulSoup

from app.services.dbFuncs import getDataFromDB
from app.config import settings

def extractAddress(div):
    if not div:
        return ""
    
    addressLines = [line.strip() for line in div.text.split("\n") if line.strip()]

    return " ".join(addressLines) if addressLines else ""

def getCompanyDetails(pageLink):
    try:
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Referer': 'https://search.sunbiz.org/Inquiry/CorporationSearch/SearchResults/EntityName/random/Page1?searchNameOrder=RANDOM',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Sec-GPC': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36',
            'sec-ch-ua': '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"'
        }
        
        cookies = {
            'ARRAffinity': '3901091b91d88a130095cf3c0d37c7fb2a43c68507d0526e6912b513f21b0d7e',
            'ARRAffinitySameSite': '3901091b91d88a130095cf3c0d37c7fb2a43c68507d0526e6912b513f21b0d7e'
        }

        searchResults = requests.get(pageLink, headers=headers, cookies=cookies, allow_redirects=True)
        searchResults.raise_for_status() # throw error if any status code other than 200

        soup = BeautifulSoup(searchResults.text, 'html.parser')

        companyDetails = {
            "filingInformation": {},
            "principalAddress": "",
            "mailingAddress": "",
            "registeredAgent": "",
            "officers": [],
            "annualReports": [],
            "documentImages": ""
        }

        # Extract Filing Information
        filing_div = soup.find('div', class_='filingInformation')
        if filing_div:
            info_div = filing_div.find('div')
            if info_div:
                labels = info_div.find_all('label')
                spans = info_div.find_all('span')
                for label, span in zip(labels, spans):
                    key = label.text.replace(':', '').strip()
                    value = span.text.strip()
                    companyDetails["filingInformation"][key] = value
        
        # Extract Detail Sections
        detail_sections = soup.find_all('div', class_='detailSection')
        
        # Process each section based on its content
        for section in detail_sections:
            sectionTitleSpan = section.find('span')
            if not sectionTitleSpan:
                continue
                
            sectionTitle = sectionTitleSpan.text.strip()
            
            if sectionTitle == 'Principal Address':
                innerDiv = section.find('div')
                if innerDiv:
                    companyDetails["principalAddress"] = extractAddress(innerDiv)
            
            elif sectionTitle == 'Mailing Address':
                innerDiv = section.find('div')
                if innerDiv:
                    companyDetails["mailingAddress"] = extractAddress(innerDiv)
            
            elif sectionTitle == 'Registered Agent Name & Address':
                spans = section.find_all('span')
                agent_name = spans[1].text.strip() if len(spans) > 1 else ""
                agent_address = extractAddress(section.find('div'))
                companyDetails["registeredAgent"] = {
                    "name": agent_name,
                    "address": agent_address
                }
            
            elif sectionTitle == 'Officer/Director Detail':
                officers = []
                current_officer = {}
                
                for element in section.children:
                    if element.name == 'span':
                        text = element.text.strip()
                        if 'Title' in text:
                            if current_officer and current_officer.get('name'):
                                officers.append(current_officer)
                            current_officer = {"title": text.replace('Title', '').strip()}
                        elif element.find('div'):
                            current_officer["address"] = extractAddress(element.find('div'))
                    elif isinstance(element, str) and element.strip():
                        stripped_text = element.strip()
                        if current_officer and "name" not in current_officer and stripped_text:
                            current_officer["name"] = stripped_text
                
                if current_officer and current_officer.get('name'):
                    officers.append(current_officer)
                companyDetails["officers"] = officers
            
            elif sectionTitle == 'Annual Reports':
                reports = []
                table = section.find('table')
                if table:
                    rows = table.find_all('tr')[1:]  # Skip header row
                    for row in rows:
                        cells = row.find_all('td')
                        if len(cells) == 2:
                            reports.append({
                                "year": cells[0].text.strip(),
                                "filed_date": cells[1].text.strip()
                            })
                companyDetails["annualReports"] = reports
            
            elif sectionTitle == 'Document Images':
                table = section.find('table')
                documentImages = []
                if table:
                    rows = table.find_all('tr')[1:]
                    rowData = {}
                    for row in rows:
                        cells = row.find_all('td')
                        if len(cells) == 2:
                            link = cells[1].find('a')
                            rowData["url"] = link.get('href')
                            rowData["name"] = cells[0].text.strip()
                            documentImages.append(rowData)
                companyDetails["documentImages"] = documentImages

        return companyDetails
    except Exception as e:
        print("Error while crawling data", e)
        return e

async def crawlWebsiteForData(searchRequest: SearchRequestDTO):

    print("Started crawling for", searchRequest.term)

    # url = "https://search.sunbiz.org/Inquiry/CorporationSearch/ByName"
    url = settings.COMPANY_DETAILS_URL

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://search.sunbiz.org",
        "Pragma": "no-cache",
        "Referer": "https://search.sunbiz.org/Inquiry/CorporationSearch/ByName",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Sec-GPC": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
        "sec-ch-ua": '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"'
    }
    
    data = {
        "SearchTerm": searchRequest.term,
        "InquiryType": "EntityName",
        "SearchNameOrder": ""
    }

    try:
        response = requests.post(url, headers=headers, data=data, allow_redirects=True)
        response.raise_for_status() # throw error if any status code other than 200

        print("Crawling completed for", searchRequest.term)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('div', id='search-results')

        resultData = []
        if results:
            table = results[0].find('table')
            if  table:                
                tbody = table.find('tbody')
                if tbody:
                    for row in tbody.find_all('tr'):
                        rowData = {
                            "name": "",
                            "documentNumber": "",
                            "status": "",
                            "detailsUrl": "",
                            "details": {}
                        }
                        columns = row.find_all('td')
                        rowData["name"] = columns[0].find('a').text.strip()  # Extracting name from <a> tag
                        rowData["documentNumber"] = columns[1].text.strip()         # Extracting document number
                        rowData["status"] = columns[2].text.strip()                 # Extracting status
                        link = columns[0].find('a')
                        if link:
                            companyBaseUrl = settings.COMPANY_DETAILS_URL
                            pageLink = f"""{companyBaseUrl}?{link.get('href').split("?")[1]}"""
                            details = getCompanyDetails(pageLink)
                            rowData["detailsUrl"] = pageLink
                            rowData["details"] = details
                        
                        resultData.append(rowData)
        
        print("Returning data for", searchRequest.term)
        return resultData
    except Exception as e:
        print("Error encountered while crawling data",e)
        return {"message": "Error while processing request", "error": e}