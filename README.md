# Network Incident Reporting System

A full-stack web application for reporting, managing, and tracking network incidents. This system features secure user authentication, incident CRUD operations, and a modern frontend interface.

---

## Features

- User registration and login with JWT authentication
- Create, view, update, and delete network incidents
- Role-based access control (default: engineer)
- MongoDB Atlas cloud database integration
- RESTful API with FastAPI
- Frontend built with React (Vite)
- Deployment-ready for Render

---

## Tech Stack

### Backend
- FastAPI (Python)
- MongoDB Atlas (cloud)
- PyMongo
- python-jose (JWT)
- Passlib (password hashing)

### Frontend
- React (Vite)
- JavaScript
- Fetch API

### Deployment
- GitHub
- Render

---

## Project Structure

```
powernasriharigalan_SWS212Lab3/
│
├── backend/
│   ├── auth.py
│   ├── database.py
│   ├── incidents.py
│   ├── jwt_utils.py
│   ├── main.py
│   ├── models.py
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── ...
│
├── .gitignore
├── README.md
```

---

## Backend Setup

1. Navigate to the backend folder:
	```bash
	cd backend
	```
2. Create a virtual environment:
	```bash
	python -m venv .venv
	```
3. Activate the environment:
	- **Windows (PowerShell):**
	  ```powershell
	  .venv\Scripts\Activate.ps1
	  ```
	- **Windows (cmd):**
	  ```cmd
	  .venv\Scripts\activate.bat
	  ```
	- **macOS/Linux:**
	  ```bash
	  source .venv/bin/activate
	  ```
4. Install dependencies:
	```bash
	pip install -r requirements.txt
	```
5. Set environment variables (do NOT hardcode values):
	- `MONGO_URI=YOUR_MONGO_URI`
	- `SECRET_KEY=YOUR_SECRET_KEY`
	- `ALGORITHM=HS256`
	- `ACCESS_TOKEN_EXPIRE_MINUTES=30`

---

## Frontend Setup

1. Navigate to the frontend folder:
	```bash
	cd frontend
	```
2. Install dependencies:
	```bash
	npm install
	```
3. Start the development server:
	```bash
	npm run dev
	```

---

## API Endpoints (Sample)

| Method | Endpoint              | Description                  |
|--------|----------------------|------------------------------|
| POST   | /auth/register       | Register a new user          |
| POST   | /auth/login          | User login (JWT)             |
| GET    | /incidents/          | List all incidents           |
| POST   | /incidents/          | Create a new incident        |
| GET    | /incidents/{id}      | Get incident by ID           |
| PUT    | /incidents/{id}      | Update incident by ID        |
| DELETE | /incidents/{id}      | Delete incident by ID        |

---

## Deployment (Render)

1. Push your code to a GitHub repository.
2. Create a new web service on [Render](https://render.com/):
	- Connect your GitHub repo.
	- Set the build and start commands for backend:
	  - **Build Command:** `pip install -r requirements.txt`
	  - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port 10000`
	- Add environment variables in the Render dashboard:
	  - `MONGO_URI=YOUR_MONGO_URI`
	  - `SECRET_KEY=YOUR_SECRET_KEY`
	  - `ALGORITHM=HS256`
	  - `ACCESS_TOKEN_EXPIRE_MINUTES=30`
3. For the frontend, deploy as a static site:
	- **Build Command:** `npm run build`
	- **Publish Directory:** `dist`

---

**Note:**
- Never commit real credentials or secrets to your repository.
- Use environment variables for all sensitive information.
- Replace all placeholders (e.g., `YOUR_MONGO_URI`, `YOUR_SECRET_KEY`) with your actual values in the deployment environment only.