# Vertical Slice Architecture

## Project Structure

Each feature is self-contained with:

```bash
app/features/<feature_name>/
├── __init__.py         # Package initialization and registration
├── models.py           # Data models and database interactions
├── services.py         # Business logic and core functionality
├── views.py            # Route handlers and request processing
└── template/           # Frontend assets
    ├── index.html      # Main template for the feature
    └── js/
        └── new_feature.js  # Feature-specific JavaScript
```

Detailed instructions for LLMs can be found in the [**feature_conventions.md**](./feature_conventions.md) file in the root project directory.

## Setup Instructions

1. **Clone the repository**
2. **Create a virtual environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the environment**

   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**

   ```bash
   ./run.sh
   # or
   flask run
   ```

6. **Run the application**

   ```bash
   http://localhost:5000/
   ```
