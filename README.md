# E-Commerce Nexus Backend

## Overview

The E-Commerce Nexus Backend is a robust and scalable backend system for managing an e-commerce platform. Built using Django and Django REST Framework, it provides APIs for product management, user authentication, cart operations, order processing, and more. The backend is designed to be deployed on modern cloud platforms like Vercel.

## Features

- **User Authentication**: Secure user registration, login, and profile management.
- **Product Management**: CRUD operations for products and categories.
- **Cart Operations**: Add, update, and delete items in the cart.
- **Order Processing**: Manage orders and payments.
- **Search and Metrics**: Unified search and product metrics.
- **API Documentation**: Swagger and Redoc integration for comprehensive API documentation.

## Technologies Used

- **Framework**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **API Documentation**: Swagger (drf-yasg)
- **Deployment**: Vercel

## Installation

### Prerequisites

- Python 3.8 or higher
- PostgreSQL
- Node.js (for Vercel CLI)

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/KelvinOnyango/alx_ecommerce_nexus_project.git
   cd alx_ecommerce_nexus_project
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configure the database:

   - Update `DATABASES` in `settings.py` with your PostgreSQL credentials.

4. Apply migrations:

   ```bash
   python manage.py makemigrations
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

## API Endpoints

### Authentication

- `POST /api/auth/register/`: Register a new user.
- `POST /api/auth/login/`: Login and obtain JWT tokens.

### Products

- `GET /api/products/`: List all products.
- `POST /api/products/`: Create a new product.
- `GET /api/products/<id>/`: Retrieve, update, or delete a product.

### Cart

- `GET /api/cart/`: Retrieve the user's cart.
- `POST /api/cart/`: Add items to the cart.
- `PATCH /api/cart/`: Update cart items.
- `DELETE /api/cart/`: Remove items from the cart.

### Orders

- `GET /api/orders/`: List all orders.
- `POST /api/orders/`: Create a new order.

### Metrics and Search

- `GET /api/stats/products/`: Retrieve product metrics.
- `GET /api/search/`: Perform a unified search.

## Deployment

### Deploying to Vercel

1. Install the Vercel CLI:

   ```bash
   npm install -g vercel
   ```

2. Create a `vercel.json` file:

   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "manage.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "manage.py"
       }
     ]
   }
   ```

3. Deploy the project:

   ```bash
   vercel
   ```

4. Access your project at the provided Vercel URL.

## API Documentation

- Swagger: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- Redoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the BSD License.

## Contact

For support or inquiries, please contact [support@example.com](mailto:support@example.com).
