# SNYK_PROBELY Test

---

# Probely Findings Integration API

Django project that fetches and lists security findings from the [Probely API](https://developers.probely.com/) using a management command and views.

---

## Features

- Retrieves and stores all findings from the Probely API for a given target
- Management command for importing findings from the external API (Probely)
- REST API endpoint to list findings (query parameters supported: `definition_id`, `scan`, and `include_list_scans`)
- SQLite database used
- Django admin
- Swagger/OpenAPI documentation with examples

---

## Installation steps

Follow these steps to run the project locally using Docker.

NOTE: Docker & Docker compose are needed (tips should come by default with Docker Desktop)

### 1- Github: clone the repo

```bash
git clone
```

Then go into the project:

```bash
cd
```

---

### 2- Preliminary step .env

At the project root (same level as `manage.py`), copy the `.env.example` and create your own `.env`:

```bash
cp .env.example .env
```

Update the `.env` with the **Probely API key** and base URL provided in the test (to avoid commit this JWT to GitHub...):

```env
PROBELY_API_KEY=your_provided_jwt_token
PROBELY_API_BASE_URL =https://api.probely.com
PROBELY_DEFAULT_TARGET_ID=Tt2f8EyPSTwq
```

---

### 3. Build and run the Docker containers

```bash
docker compose build
docker compose up
```

This will:

- Build the Django app container
- Start the web service with SQLite as database (no external DB needed)

---

### 4. Apply migrations

In a separate terminal, run:

```bash
docker compose exec snyk_django python manage.py migrate
```

NOTE "snyk_django" is the docker service name.

After running migrations, it's good to go.

---

## Using the API

Once running, the API will be available at:

```
http://localhost:8000/api/findings/
```

### Example queries

- List all findings:

  ```
  http://localhost:8000/api/findings/
  ```

- Filter by `definition_id`:

  ```
  http://localhost:8000/api/findings/?definition_id=TTmdzcaxWqxj
  ```

- Filter by `scan`:

  ```
  http://localhost:8000/api/findings/?scan=1c6umSqQf1G7
  ```

- Reduce payload (exclude `scans` field - optional param, for readability & testing purposes...):

  ```
  http://localhost:8000/api/findings/?include_list_scans=false
  ```

---

### API Documentation (Swagger UI docs)

For convinience, you can check out the swagger doc link below for testing.
The documentation also includes some explanations and details about the query parameters (and other options).

Swagger doc link:

```
http://localhost:8000/api/docs/
```

How to:

- Click on the API for 'findings' and click on "Try it out".
- Modify the parameters if needed
- Click on "Execute". The result will appear in the Responses section.

## Questions

In case of any doubt, problem during installation or question, feel free to reach out to me!
Thanks!
