# small-post-API

A FastAPI/SQLAlchemy learning API with account registration/login, bearer-token current-user lookup, and post create/list/read/update/delete endpoints.

## Local setup

Use Python 3 compatible with the historical pinned dependencies in `requirements.txt`. In an activated virtual environment, run `python -m pip install -r requirements.txt`, review database initialization/settings in `database.py` and `services.py`, then start `uvicorn app:app --reload`. Swagger is available at `http://127.0.0.1:8000/docs`.

The registration route is spelled `/api/regeister` in source; login uses OAuth2 form fields, not an arbitrary JSON body. Routes are in `app.py` and payload models in `schemas.py`.

Keep it local with dummy data. Authentication dependencies do not establish post ownership checks: update/delete actions need authorization review. CORS is permissive and JWT dependencies are old. Build, authentication, and database behavior were not verified. The original hosted documentation link below is retained, not confirmed live.

to try API: https://post-app-fastapi.herokuapp.com/docs
