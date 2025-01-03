# Web Analysis Application

This project is a FastAPI (backend) and Next.js (frontend) application designed to scrape websites and generate comprehensive reports. It takes a website URL as input, scrapes the site using a multi-agent system (CrewAI), and produces three types of reports:

- **Frontend Report**
- **UI/UX Report**
- **SEO Report**

The main tools used include:
- CrewAI
- Jina AI
- PageSpeed Insights API
- OpenAI

---

## Setting Up the Project Locally

### Prerequisites
1. **Python environment**: Create a virtual environment by running:
   ```bash
   python -m venv .venv
   ```
   Then activate the virtual environment:
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. **Node.js environment**: Ensure you have Node.js installed for the frontend.

### Backend Setup
1. Navigate to the backend directory `Report-Generator-main`.
2. Create a `.env` file in the same directory with the following keys:
   ```env
   GROQ_API_KEY=<groq_key>
   VISION_MODEL=<groq_model_name>  # Use this if you plan to work with llama as the vision LLM
   PAGESPEED_INSIGHTS_API_KEY=<pagespeedinsights_key>
   OPENAI_API_KEY=<openai_api_key>
   JINA_AI_API_KEY=<jinaai_api_key>
   ```
3. Run the backend server:
   ```bash
   uvicorn app:app --reload
   ```

### Frontend Setup
1. Navigate to the `frontend` directory.
2. Create a `.env.local` file with the following content:
   ```env
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   ```
3. Install dependencies and start the development server:
   ```bash
   npm install
   npm run dev
   ```

---

## Running the Project with Docker

### Backend
1. Create the `.env` file in the `Report-Generator-main` directory as mentioned above.
2. Build the Docker image:
   ```bash
   docker build -t fastapi-backend .
   ```
3. Run the Docker container:
   ```bash
    docker run -d -p 8000:8000 fastapi-backend
   ```

### Frontend
1. Create the `.env.local` file in the `frontend` directory as mentioned above.
2. Build the Docker image:
   ```bash
   docker build -t nextjs-frontend .
   ```
3. Run the Docker container:
   ```bash
   docker run -p 3000:3000 nextjs-frontend
   ```

---

By following these steps, you can set up and run the Web Analysis Application locally or in a Dockerized environment.

