# Clinical AI Prototypes: EMR Automation and Analysis

### Project Structure
#### The repository is organized into two main folders, one for each task.

```bash
├── Task1/
│   ├── main.py
│   ├── services.py
│   ├── models.py
│   └── README.md  (Detailed instructions for Task 1)
│
├── Task2/
│   ├── main.py
│   ├── processor.py
│   ├── pdf_parser.py
│   └── README.md  (Detailed instructions for Task 2)
│
└── README.md      (This file)
```


### The Prototypes
1. Task 1: Ambient Listening EMR Prototype
    Goal: To automatically transcribe a doctor-patient audio consultation and extract structured clinical notes (Chief Complaint, History, Diagnosis, Plan) into a JSON format.

    Core AI: OpenAI Whisper for transcription and Google Gemini for analysis.

    For more details, see the Task 1 README.

2. Task 2: Patient Data Processor & Lab Trend Analyzer
    A two-part tool to (1) summarize multiple structured EMR visit files into a single narrative and (2) parse PDF lab reports to extract and visualize trends over time.

    Core AI: Google Gemini for both narrative summarization and PDF data extraction.

    For more details, see the Task 2 README.

    Getting Started
    Follow these steps to set up and run the applications on your local machine.



### 1. Clone the Repository
```bash
git clone <repository-url>
```

### 2. Set up the Python Environment
```
This project uses uv for fast and efficient package management.
```

### 3. Create the virtual environment
```bash
uv venv

# Activate the environment (on macOS/Linux)
source .venv/bin/activate

# Activate the environment (on Windows)
.venv\Scripts\activate
```

### 4. Running the Applications
```bash
./start.sh
```