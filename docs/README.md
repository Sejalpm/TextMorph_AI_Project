nlp_project/
├── config/
│   └── config.yaml                     # 🔧 Centralized configuration for models, paths, app settings
├── src/                                # 📦 Core source code package
│   ├── __init__.py                     # Makes 'src' a Python package
│   ├── components/                     # 🧩 Individual, reusable NLP components
│   │   ├── __init__.py
│   │   ├── data_handler.py             # 📥 Handles data ingestion (Hugging Face datasets, local files: PDF, DOCX, TXT)
│   │   ├── text_preprocessing.py       # 🧹 Text cleaning and preprocessing routines
│   │   ├── summarizer.py               # 📝 Implements abstractive (BART, T5) and extractive summarization
│   │   ├── paraphraser.py              # ✍️ Implements T5-based text paraphrasing with diversity options
│   │   ├── similarity_checker.py       # ✅ Measures semantic similarity using SentenceTransformers
│   │   └── evaluation.py               # 📊 Contains functions for ROUGE, BLEU, and other evaluation metrics
│   ├── pipeline/                       # 🔄 Orchestration layer for combining components
│   │   ├── __init__.py
│   │   ├── main_pipeline.py            # 🎯 Orchestrates the overall summarization/paraphrasing workflow (backend logic)
│   │   └── web_app_pipeline.py         # 🌐 Specific pipeline logic for the web application (Streamlit/Flask interface)
│   ├── config_manager.py               # ⚙️ Utility for loading and managing configurations from config.yaml
│   ├── logging_system.py               # 📝 Centralized logging utility
│   ├── exceptions.py                   # ⚠️ Custom error handling for specific project exceptions
│   ├── utils.py                        # 🛠️ General utility functions (e.g., file export, progress indication)
│   └── app.py                          # 🚀 Main entry point for the Streamlit web application (or Flask/FastAPI app)
├── artifacts/                          # 💾 Storage for generated outputs (e.g., cached models, sample processed data, evaluation reports)
├── notebooks/                          # 🧪 Jupyter notebooks for experimentation, model exploration, and testing
├── tests/                              # 🔍 Unit and integration tests for code reliability
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_summarizer.py          # Unit tests for summarizer component
│   │   └── test_paraphraser.py         # Unit tests for paraphraser component
│   └── integration/
│       └── test_app_workflow.py        # Integration tests for the full application flow
├── docs/                               # 📄 Project documentation files
│   ├── README.md                       # Comprehensive setup and usage guide
│   ├── API_Docs.md                     # Documentation for REST API endpoints (if Flask/FastAPI is chosen)
│   └── Technical_Report.md             # Detailed report on the architecture, models, and results
├── requirements.txt                    # 📋 Lists all Python dependencies
├── setup.py                            # 📦 Script for packaging the project as a distributable library
└── .gitignore                          # 🚫 Specifies files and directories to ignore in version control