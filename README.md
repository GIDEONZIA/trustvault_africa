# RentFlow - Property Management SaaS

A comprehensive Django-based property management system designed for the Kenyan rental market, with M-Pesa payment integration.

## Features

- **Multi-role Authentication** – Landlord, tenant, and vendor accounts with email-based login
- **Property Management** – Track properties, units, occupancy, and revenue
- **Lease Management** – Create, renew, and terminate leases with auto-generated lease numbers
- **Automated Invoicing** – Monthly rent invoice generation via Celery
- **M-Pesa Integration** – STK Push payments via Safaricom Daraja API
- **Maintenance Workflow** – Tenant requests → landlord review → vendor assignment → completion
- **Dashboard Analytics** – Revenue, collection rates, occupancy, overdue tracking
- **Public Listings** – Searchable vacant unit listings with filtering
- **REST API** – Full DRF API for all resources at `/api/v1/`
- **Responsive UI** – Tailwind CSS with HTMX for dynamic interactions

## Tech Stack

- Python 3.11+, Django 5.0, Django REST Framework
- PostgreSQL (production) / SQLite (development)
- Redis + Celery for async tasks and caching
- Tailwind CSS (CDN) + HTMX
- M-Pesa Daraja API (Sandbox & Production)

## Quick Start

```bash
# Clone the repo
git clone <repo-url>
cd rentflow

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Project Structure

```
rentflow/
├── apps/
│   ├── accounts/      # User auth, profiles
│   ├── properties/    # Properties & units
│   ├── tenants/       # Leases & tenant profiles
│   ├── invoices/      # Invoice generation & tracking
│   ├── payments/      # M-Pesa & manual payments
│   ├── maintenance/   # Maintenance requests
│   ├── dashboard/     # Analytics dashboard
│   └── public_listings/ # Public property search
├── config/
│   ├── settings/      # Environment-specific settings
│   ├── urls.py        # Root URL routing
│   ├── celery.py      # Celery configuration
│   └── wsgi.py
├── templates/         # HTML templates (Tailwind CSS)
├── static/            # Static assets
└── manage.py
```

## Celery Tasks

Start Celery worker and beat for background tasks:

```bash
celery -A config worker -l info
celery -A config beat -l info
```

Scheduled tasks:
- **Generate monthly invoices** – 1st of each month at midnight
- **Send rent reminders** – Daily at 8:00 AM
- **Mark overdue invoices** – Daily at 12:30 AM
- **Check expiring leases** – Daily at 9:00 AM

## API Endpoints

All endpoints under `/api/v1/`:

| Resource      | Endpoints                                          |
|---------------|---------------------------------------------------|
| Auth          | `POST /register/`, `POST /login/`, `POST /logout/` |
| Properties    | `GET/POST /properties/`, `GET/PUT/DELETE /properties/:id/` |
| Units         | `GET/POST /properties/:id/units/`, `GET/PUT/DELETE /units/:id/` |
| Leases        | `GET/POST /leases/`, `GET/PUT /leases/:id/`, `POST /leases/:id/terminate/`, `POST /leases/:id/renew/` |
| Invoices      | `GET/POST /invoices/`, `GET/PUT /invoices/:id/`, `POST /invoices/:id/send-reminder/`, `POST /invoices/:id/waive/` |
| Payments      | `POST /payments/initiate/`, `GET /payments/`, `GET /payments/:id/status/` |
| Maintenance   | `GET/POST /maintenance/`, `GET/PUT /maintenance/:id/`, `POST /maintenance/:id/complete/` |
| Dashboard     | `GET /dashboard/summary/` |
| Listings      | `GET /listings/`, `GET /listings/:id/` |

## M-Pesa Integration

Set these environment variables for M-Pesa:

```
MPESA_CONSUMER_KEY=your_consumer_key
MPESA_CONSUMER_SECRET=your_consumer_secret
MPESA_PASSKEY=your_passkey
MPESA_SHORTCODE=174379
MPESA_ENVIRONMENT=sandbox
MPESA_CALLBACK_URL=https://your-domain/api/v1/payments/callback/
```

## License

MIT
