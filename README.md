# Simple store
This is a simple application that has a partial implementation of an online store's functionality.
It was created to demonstrate how Domain Driven Design can be implemented using the following technologies:
- **Python** – programming language
- **FastAPI** – web framework
- **Pydantic** – library for creating models and validating them
- **SQLAlchemy** – ORM for working with a database


## Requirements for setup
- **Docker**
- **PostgreSQL**


## Setup
1. Create a database for the project.
2. Rename the `.env.example` file to `.env`:

    ```bash
    cd simple_store
    mv .env.example .env
    ```

3. Set the `DATABASE_URL` in `.env`.
   **IMPORTANT**: The `DATABASE_URL` must start with `postgresql+asyncpg:`.

4. Apply the database dump.
	```bash
	psql -d <db_name> -f db_dumps/orders.sql
	```


## Running the project
1. Navigate to the project directory:

    ```bash
    cd simple_store
    ```

2. Run the following command:

    ```bash
    make docker-run
    ```
   or alternatively, run:

    ```bash
    docker run --network=host --env-file=.env workaccpy/simple_store:latest
    ```

   **IMPORTANT**: The first time you run these commands, you must have an internet connection because the Docker image of the application is downloaded from Docker Hub.


## Endpoints

### FastAPI API Documentation

FastAPI provides automatically generated and interactive documentation for API, making it easy to explore, test,
and understand the available endpoints.
Below are the key documentation tools available by default:

#### 🚀 **Swagger UI** (`/docs`)

The [Swagger UI](https://swagger.io/tools/swagger-ui/) is available at the `/docs` endpoint.
It offers an intuitive and interactive interface where you can:

- **Visualize**: See the structure of API, with all routes and their details neatly organized.
- **Interact**: Send requests to the API directly from the browser, testing endpoints without additional tools.
- **Understand**: Quickly grasp how the API works, with descriptions of each route, parameters, and expected responses.

---

#### 🎨 **ReDoc** (`/redoc`)

At the `/redoc` endpoint, you will find [ReDoc](https://redoc.ly/), a beautifully minimal and user-friendly documentation tool.
While it doesn’t provide the interactivity of Swagger UI, it excels in presenting:

- **Clean design**: ReDoc offers a structured and modern view of the API, making it easy to browse.
- **Efficient navigation**: ReDoc’s documentation is organized into collapsible sections, perfect for quickly finding specific endpoints.

---

#### 🛠 **OpenAPI Schema** (`/openapi.json`)

The `/openapi.json` endpoint serves the complete **OpenAPI schema** for Simple Store application in JSON format.
This schema is a machine-readable representation of API, defining all endpoints, their parameters, request bodies, and responses.
It can be:

- **Used by tools**: Integrate API with tools that support OpenAPI for automation, code generation, and validation.
- **A standard**: As an OpenAPI-compliant schema, it provides a universal way to describe API for both humans and machines.

This schema powers both Swagger UI and ReDoc.

### Product Management API Documentation

This section outlines the endpoints available for managing product categories, subcategories, and products. Each endpoint supports various operations, such as creation, listing, updating, and deleting, as well as handling reservations and sales.

#### 📦 **Create Category** (`/category/create`)

- **Description**: Create a new product category.
- **Purpose**: Allows the addition of a new category to organize products.

---

#### 📋 **List Categories** (`/category/list`)

- **Description**: Retrieve a list of all product categories.
- **Purpose**: Provides a comprehensive list of existing categories for browsing or selection.

---

#### 🗂 **Create Subcategory** (`/subcategory/create`)

- **Description**: Create a new product subcategory.
- **Requirements**: At least one category must be created before adding a subcategory.
- **Purpose**: Allows for further organization of products within an existing category.

---

#### 📜 **List Subcategories** (`/subcategory/list`)

- **Description**: Retrieve a list of all product subcategories.
- **Purpose**: Provides a comprehensive list of existing subcategories for browsing or selection.

---

#### 📊 **Sales Report** (`/order/report/sales`)

- **Description**: Obtain a report of sold products with the following filters:
  - **Categories**
  - **Subcategories**
  - **Users**
  - **Products**
- **Pagination**: Supports pagination with parameters:
  - **limit**
  - **offset**
- **Purpose**: Generates a detailed sales report based on specified filters and pagination.

---

#### 🛠 **Create Product** (`/product/create`)

- **Description**: Create a new product.
- **Requirements**: At least one category and one subcategory must exist before adding a product.
- **Purpose**: Allows the addition of a new product to the inventory.

---

#### 🏷 **List Products** (`/product/list`)

- **Description**: Retrieve a list of products where the available quantity is greater than 0.
- **Filters Supported**:
  - **Categories**
  - **Subcategories**
- **Pagination**: Supports pagination with parameters:
  - **limit**
  - **offset**
- **Purpose**: Provides a comprehensive list of available products with filtering and pagination options.

---

#### 🔄 **Update Product Quantity** (`/product/update/count`)

- **Description**: Change the quantity of a product.
- **Impact**: Orders with the status "RESERVED" are canceled if the quantity is reduced to zero.
- **Purpose**: Adjusts the available quantity of a product and manages reservations accordingly.

---

#### 💲 **Update Product Price** (`/product/update/price`)

- **Description**: Change the price of a product.
- **Impact**: The price is updated in all orders with the status "RESERVED."
- **Purpose**: Updates the price of a product and reflects this change in reserved orders.

---

#### 🏷 **Update Product Discount** (`/product/update/discount`)

- **Description**: Change the discount on a product.
- **Impact**: The discount is updated in all orders with the status "RESERVED."
- **Purpose**: Adjusts the discount for a product and updates it in reserved orders.

---

#### ❌ **Delete Product** (`/product/delete`)

- **Description**: Delete a product from the inventory.
- **Impact**: All order history for the product is also deleted.
- **Purpose**: Permanently removes a product and its associated order history.

---

#### 🔒 **Reserve Product** (`/product/reserve`)

- **Description**: Reserve a product.
- **Impact**: Decreases the available quantity and creates an order with the status "RESERVED."
- **Purpose**: Marks a product as reserved and adjusts its available quantity.

---

#### 🚫 **Cancel Product Reservation** (`/product/cancel_reservation`)

- **Description**: Cancel a product reservation.
- **Impact**: Increases the available quantity and changes the order status to "CANCELLED."
- **Purpose**: Releases a reserved product and updates the order status.

---

#### 💰 **Sell Product** (`/product/sell`)

- **Description**: Sell a product.
- **Impact**: Decreases the total product quantity and changes the order status to "COMPLETED."
- **Purpose**: Finalizes the sale of a product and updates its quantity and order status.
