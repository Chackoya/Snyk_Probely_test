# SNYK_PROBELY Test

---

# Probely Findings Integration API

Django project that fetches and lists security findings from the [Probely API](https://developers.probely.com/) using a management command and views.

This README will explain how to install the project and how to run it.

---

## Features

- Retrieves and stores all findings from the Probely API for a given target
- Management command for importing findings from the external API (Probely)
- REST API endpoint to list findings (query parameters supported: `definition_id`, `scan`, and `include_list_scans`)
- SQLite database used
- Django admin
- Swagger/OpenAPI documentation with examples
- Docker app

---

## Installation steps

Follow these steps to run the project locally using Docker.

NOTE: Docker & Docker compose are needed (tips should come by default with Docker Desktop)

### 1- Github: clone the repo

```bash
git clone https://github.com/Chackoya/Snyk_Probely_test.git
```

Then go into the project:

```bash
cd Snyk_Probely_test
```

---

### 2- Preliminary step .env (IMPORTANT)

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

### 3- Build and run the Docker containers

```bash
docker compose build
docker compose up
```

This will:

- Build the Django app container
- Start the web service with SQLite as database (no external DB needed)

---

### 4- Apply migrations

In a separate terminal, run:

```bash
docker compose exec snyk_django python manage.py migrate
```

NOTE "snyk_django" is the docker service name.

After running migrations, it's good to go.

---

### 5- Optional - Django Admin Access

To access the Django admin panel (to check the Findings):

1. Create a superuser:

   ```bash
   docker compose exec snyk_django python manage.py createsuperuser
   ```

2. Follow the prompts (username, email, password)

3. Visit the admin interface:

   ```
   http://localhost:8000/admin/
   ```

4. Log in with the credentials you just created

5. In the django admin you can see the model Finding and the data entries.

## Fetch Findings from Probely

To import findings from the Probely API using the Django command:

```bash
docker compose exec snyk_django python manage.py fetch_target_findings
```

Optionally specify a target ID:

```bash
docker compose exec snyk_django python manage.py fetch_target_findings --target=Tt2f8EyPSTwq
```

NOTE: without the input --target, the command will execute the code for the target specified on the .env (for the purpose of this test). But you can add a new target as shown above.

## Using the API

The API to obtain the findings will be available at:

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

- Click on the API for 'findings' (GET) and click on "Try it out".
- Modify the parameters if needed
- Click on "Execute". The result will appear in the Responses section.

NOTE: for full listing of findings, it might take sometime to render on swagger UI due to the quantity of data... but the API is still fast on other api testing tools.

## Questions

In case of any doubt, problem during installation or question, feel free to reach out to me!
Thanks!
