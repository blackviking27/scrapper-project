# Online Scrapper

## Introduction
This project consists of a frontend and backend application that communicate with each other. The backend is built using Python, and the frontend is built using JavaScript. We will use PostgreSQL as our database, running in a Docker container.

## Prerequisites
- Docker installed on your machine
- Node.js and npm installed for the frontend
- Python installed for the backend
- Git for version control

## Setting Up PostgreSQL with Docker
1. **Pull the PostgreSQL Docker image:**  
   Open your terminal and run:
   ```bash
   docker pull postgres:latest
   ```

2. **Run the PostgreSQL container:**  
   Execute the following command to start a PostgreSQL container:
   ```bash
   docker run --name postgres-db -e POSTGRES_PASSWORD=yourpassword -p 5432:5432 -d postgres
   ```  
   Replace `yourpassword` with your desired credentials. The `-d` flag runs the container in the background. The postgres-db container will be accessible on port **5432**.
   
   <br>

3. **Verify that PostgreSQL is running:**  
   You can check the running containers with:
   ```bash
   docker ps
   ```

## Setting Up Environment Variables

## Setting up project for Local Development

### Backend Setup
1. **ENV variables required for the backend**  
   - Add the following lines:
     ```env
     POSTGRES_USER=postgres
     POSTGRES_PASSWORD=<yourpassword>
     POSTGRES_SERVER=localhost
     POSTGRES_PORT=5432
     POSTGRES_DB=<yourdbname>
     WEBSITE_DATA_URL=https://search.sunbiz.org/Inquiry/CorporationSearch/ByName
     COMPANY_DETAILS_URL=https://search.sunbiz.org/Inquiry/CorporationSearch/SearchResultDetail
     ```

## Backend

### Creating virtual environment
Create a virtual enviroment to isolate dependencies and run the backend application. Inside the `backend` directory, run:

```bash
python3 -m venv .venv
```

**Activate the virtual environment:**  
   ```bash
   source .venv/bin/activate
   ```

### Backend Setup

1. **Navigate to the backend directory:**  
   ```bash
   cd backend/app
   ```

2. **Install dependencies:**  
   Make sure you have a `requirements.txt` file in your backend directory. Run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the backend application:**  
   ```bash
   fastapi dev app/main.py
   ```

## Frontend


### Frontend ENV setup

Create a `.env` file in the `frontend` directory.

**ENV variables required for the frontend**

   - Add the following lines:
     ```env
     REACT_APP_BACKEND_URL=http://localhost:8000
     ```
### Frontend Setup
1. **Navigate to the frontend directory:**  
   ```bash
   cd frontend
   ```

2. **Install dependencies:**  
   Run the following command to install the frontend dependencies:
   ```bash
   npm install
   ```

4. **Run the frontend application:**  
   ```bash
   npm run start
   ```

## Running the Applications
- Ensure that the PostgreSQL Docker container is running.
- Start the backend application first, followed by the frontend application.
- You can access the frontend at `http://localhost:3000`.

## Conclusion
You now have both the frontend and backend applications set up and communicating with each other through a PostgreSQL database running in Docker. If you have any issues, please check the logs for both the backend and frontend applications for more information.
