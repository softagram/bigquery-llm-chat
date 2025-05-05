# BigQuery Chat Agent

A simple web service using FastAPI and LangChain to interact with an LLM agent connected to Google BigQuery, with a Streamlit frontend.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Google Cloud authentication:**
    Ensure you have authenticated with Google Cloud. The easiest way is often using the gcloud CLI:
    ```bash
    gcloud auth application-default login
    ```
    Alternatively, set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of your service account key file.

5.  **Configure environment variables:**
    Create a `.env` file in the root directory and add your Google Cloud Project ID:
    ```
    GOOGLE_CLOUD_PROJECT=your-gcp-project-id
    # Optional: Specify BIGQUERY_DATASET if you want to limit the agent to a specific dataset
    # BIGQUERY_DATASET=your_dataset_name
    # Optional: Specify backend PORT if needed (default is 8080)
    # PORT=8000
    # Optional: Specify backend URL if running elsewhere
    # BACKEND_URL=http://your-backend-host:port/chat
    ```

## Running the Service

1.  **Start the Backend (FastAPI):**
    Open a terminal, navigate to the project directory, and run:
    ```bash
    python3 main.py
    # or using uvicorn for development with auto-reload
    # uvicorn main:app --reload --port 8080
    ```
    Keep this terminal running.

2.  **Start the Frontend (Streamlit):**
    Open a *second* terminal, navigate to the project directory, and run:
    ```bash
    streamlit run frontend.py
    ```
    Streamlit will open the chat interface in your web browser.

## Usage

Interact with the chat interface that opens in your browser. Ask questions about the data in your BigQuery project/dataset.

Alternatively, you can still send POST requests directly to the backend `/chat` endpoint:

```bash
curl -X POST "http://localhost:8080/chat" \
     -H "Content-Type: application/json" \
     -d '{
           "message": "Your question for the agent, e.g., How many tables are in the dataset?"
        }'
```

Replace `"Your question for the agent..."` with your actual query. 