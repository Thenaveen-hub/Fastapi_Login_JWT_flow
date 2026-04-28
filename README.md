# FastAPI Login Authentication System

A simple yet robust REST API built with FastAPI that provides user authentication using JWT tokens. This project demonstrates best practices for user registration, login, password management, and protected routes using modern Python web development technologies.

## Features

- **User Registration** - Sign up with full name, email, and password
- **User Login** - Authenticate and receive JWT access tokens
- **JWT Authentication** - Secure stateless authentication with JSON Web Tokens
- **Password Hashing** - Secure password storage using bcrypt
- **Password Change** - Update password with current password verification
- **User Management** - List and delete users (admin functionality)
- **SQLite Database** - Simple file-based database using SQLAlchemy ORM
- **Pydantic Validation** - Request/response validation with automatic type checking
- **bcrypt Security** - Industry-standard password hashing (with 72-byte limit handling)

## Tech Stack

| Technology | Purpose |
|------------|---------|
| [FastAPI](https://fastapi.tiangolo.com/) | Modern, fast web framework for building APIs |
| [SQLAlchemy](https://www.sqlalchemy.org/) | SQL toolkit and ORM for database operations |
| [Pydantic](https://pydantic.dev/) | Data validation using Python type hints |
| [Passlib](https://passlib.readthedocs.io/) | Password hashing library (bcrypt) |
| [PyJWT](https://pyjwt.readthedocs.io/) | JSON Web Token encoding/decoding |
| [SQLite](https://www.sqlite.org/) | Lightweight, serverless database |

## Project Structure

```
fastapi_login/
├── main.py              # FastAPI application with all endpoints
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic request/response schemas
├── auth_handler.py      # JWT and password hashing utilities
├── database.py          # Database connection and session management
├── test.db              # SQLite database file (auto-generated)
└── README.md            # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fastapi_login
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```
   
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic[email] passlib[bcrypt] python-jwt
   ```

## Usage

### Start the Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Interactive API Documentation

FastAPI automatically generates interactive documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/signup` | Register a new user | No |
| POST | `/login` | Authenticate and get JWT token | No |

### User Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/users` | List all registered users | No* |
| PUT | `/user/change-password` | Change user password | No* |
| DELETE | `/user/delete/{user_id}` | Delete a user by ID | No* |

*Note: These endpoints currently don't require authentication for simplicity. In production, add JWT dependency protection.

### Request Examples

#### Sign Up
```bash
curl -X POST "http://localhost:8000/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "fullname": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

#### Login
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

#### Change Password
```bash
curl -X PUT "http://localhost:8000/user/change-password?email=john@example.com&current_password=securepassword123&new_password=newpassword456" \
  -H "Content-Type: application/json"
```

#### List Users
```bash
curl -X GET "http://localhost:8000/users"
```

#### Delete User
```bash
curl -X DELETE "http://localhost:8000/user/delete/1"
```

## Database Schema

### User Model

| Field | Type | Description |
|-------|------|-------------|
| id | Integer (PK) | Auto-incrementing primary key |
| fullname | String | User's full name |
| email | String (Unique) | User's email address (indexed) |
| hashed_password | String | bcrypt hashed password |

## Security Considerations

- **Password Hashing**: Uses bcrypt with automatic salting
- **bcrypt 72-byte Limit**: Passwords are truncated to 72 characters to prevent bcrypt's internal limitation
- **JWT Tokens**: Tokens expire after 1 hour
- **Input Validation**: Pydantic validates email format and required fields

### Production Recommendations

Before deploying to production:

1. **Change the JWT Secret**: Update `JWT_SECRET` in `auth_handler.py` to a strong random key
2. **Use Environment Variables**: Store secrets in `.env` files (use `python-dotenv`)
3. **Enable CORS**: Configure allowed origins in FastAPI
4. **Add Rate Limiting**: Prevent brute force attacks
5. **Use HTTPS**: Always use TLS in production
6. **Add Authentication to Protected Routes**: Implement JWT dependency for user management endpoints
7. **Database Migration**: Consider using Alembic for database migrations
8. **Switch to PostgreSQL**: SQLite is fine for development, but use PostgreSQL/MySQL for production

## Environment Variables

Create a `.env` file:

```
JWT_SECRET=your-super-secret-key-here
DATABASE_URL=sqlite:///./test.db
```

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Author

Your Name - [@Thenaveen-hub](https://github.com/Thenaveen-hub)

## Acknowledgments

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [JWT.io](https://jwt.io/) - JSON Web Tokens introduction
