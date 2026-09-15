# Agent AI

Agent AI is a Django REST API for organization-based client management, document handling, AI-generated proposals, and Twilio SMS notifications.

## Features

- JWT authentication for users and organizations
- Organization-scoped clients, documents, proposals, and AI executions
- AI-assisted proposal generation from site-walk notes and pricing catalogs
- Proposal sections, line items, versions, approvals, and totals
- Twilio outbound SMS and inbound SMS webhook support
- PostgreSQL database configuration through environment variables

## Requirements

- Python 3.13 or compatible Python version
- PostgreSQL
- OpenAI API credentials for proposal generation
- Twilio credentials for SMS features

## Setup on Windows

From the project root:

```powershell
.\env\Scripts\Activate.ps1
```

If the virtual environment does not exist, create one and install the project dependencies:

```powershell
py -m venv env
.\env\Scripts\Activate.ps1
pip install django djangorestframework djangorestframework-simplejwt psycopg[binary] python-dotenv twilio openai pydantic
```

Create a `.env` file in the project root. Do not commit this file.

```env
DEBUG=True
SECRET_KEY=replace-with-a-long-random-secret
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=agent_ai
DB_USER=postgres
DB_PASSWORD=your-database-password
DB_HOST=127.0.0.1
DB_PORT=5432

OPENAI_API_KEY=your-openai-api-key

TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=+15551234567
```

Run migrations and start the development server:

```powershell
python manage.py migrate
python manage.py runserver
```

The API is available at `http://127.0.0.1:8000/`.

## Authentication

Register an organization owner:

```http
POST /auth/account/register/
Content-Type: application/json
```

```json
{
  "username": "owner",
  "email": "owner@example.com",
  "password": "Use-a-strong-password-123!",
  "password_confirm": "Use-a-strong-password-123!",
  "first_name": "Project",
  "last_name": "Owner",
  "organization": "Example Landscapes"
}
```

Obtain JWT access and refresh tokens:

```http
POST /auth/account/login/
Content-Type: application/json
```

```json
{
  "username": "owner",
  "password": "Use-a-strong-password-123!",
  "organization": "Example Landscapes"
}
```

Send the access token with protected requests:

```http
Authorization: Bearer <access-token>
```

Other account endpoints:

- `POST /auth/account/refresh/`
- `GET /auth/account/me/`

New registrations cannot join an existing organization by name. Use an invitation or administrator workflow for additional members.

## API Endpoints

### Clients

- `GET /api/client/create-list/`
- `POST /api/client/create-list/`
- `GET /api/client/<id>/`
- `PUT/PATCH /api/client/<id>/`
- `DELETE /api/client/<id>/`

Client phone numbers should use E.164 format, for example `+15551234567`.

### Documents

- `GET /api/document/create-list/`
- `POST /api/document/create-list/`
- `GET /api/document/<id>/`
- `PUT/PATCH /api/document/<id>/`
- `DELETE /api/document/<id>/`

Uploaded files are limited to 10 MB.

### Proposals

The proposal viewset is available at:

- `GET/POST /api/proposal/proposals/`
- `GET/PUT/PATCH/DELETE /api/proposal/proposals/<id>/`
- `POST /api/proposal/proposals/<id>/approve/`
- `POST /api/proposal/proposals/<id>/generate/`

Proposal generation uses active pricing items belonging to the authenticated user's organization. Regenerating a proposal replaces generated sections and line items and creates a new version.

### AI Executions

- `GET/POST /api/ai/ai-executions/`
- `GET /api/ai/ai-executions/<id>/`

### SMS

Send an SMS to a client:

```http
POST /api/integration/clients/<client_id>/sms/
Content-Type: application/json
Authorization: Bearer <access-token>
```

```json
{
  "message": "Your proposal is ready for review."
}
```

The client must belong to the authenticated user's organization and have a phone number. Twilio trial accounts can send only to verified recipient numbers.

## Twilio Webhook

Configure the Twilio messaging webhook URL as:

```text
https://your-public-domain.example/api/integration/twilio/webhook/
```

Use `POST` and enable Twilio signature validation. The endpoint is CSRF-exempt for Twilio requests but rejects requests without a valid `X-Twilio-Signature` header.

For local development, expose the server with a tunnel such as ngrok and use the HTTPS forwarding URL in Twilio.

## Production Configuration

Set `DEBUG=False` and provide a strong `SECRET_KEY`. Production also requires:

- A real PostgreSQL database
- `ALLOWED_HOSTS`
- SMTP settings: `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, and `EMAIL_HOST_PASSWORD`
- HTTPS at the reverse proxy or application server
- OpenAI and Twilio credentials stored outside source control

Example production checks:

```powershell
$env:DEBUG = "False"
python manage.py check --deploy
```

## Validation

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

The repository currently contains no automated test cases, so `manage.py test` reports zero tests until coverage is added.

## Project Layout

- `Agent_Ai/` - Django project configuration and root URLs
- `Accounts/` - users, organizations, registration, and JWT authentication
- `Clients/` - client records and organization-scoped access
- `Documents/` - document uploads and metadata
- `Proposals/` - proposals, pricing items, versions, and approvals
- `Ai/` - AI execution records and proposal generation agent
- `Integrations/twilio/` - Twilio client, SMS service, and inbound webhook
- `manage.py` - Django command-line entry point
