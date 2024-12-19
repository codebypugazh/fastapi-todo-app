### 1. Create virtual environment

```bash
python -m venv appenv
```
### 2. Activate virtual environment

```bash
.\appenv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. To run application

```bash
uvicorn main:app --reload
```