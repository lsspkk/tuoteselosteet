# selosteet

Tuoteselosteet Djangolla

Python 3.8.10

Tietokannassa ei mitään salaista, vain leipomotuotteita ja raaka-aineita

## Setup

### Docker Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd tuoteselosteet
```

2. Generate self-signed SSL certificates (if not present):

```bash
openssl req -x509 -newkey rsa:4096 -keyout tuoteselosteet/server.key -out tuoteselosteet/server.crt -days 365 -nodes -subj "/CN=localhost"
```

3. Build and start the containers:

```bash
docker compose up --build -d
```

4. Collect static files (Django admin CSS/JS):

```bash
docker compose exec apache python /tuoteselosteet/manage.py collectstatic --noinput
```

5. Access the application:

- Main site: https://localhost/selosteet/
- Admin panel: https://localhost/selosteet/admin/

**Note**: You'll get a security warning because of the self-signed SSL certificate. Accept it to continue.

### Local Development Setup

1. Create a virtual environment:

```bash
python3.8 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r tuoteselosteet/requirements.txt
```

3. Collect static files:

```bash
cd tuoteselosteet
python manage.py collectstatic --noinput
```

4. Run migrations:

```bash
python manage.py migrate
```

5. Create a superuser:

```bash
python manage.py createsuperuser
```

6. Run the development server:

```bash
python manage.py runserver
```
