# Patient Registration API

A FastAPI-based patient registration system with PostgreSQL, async email confirmation, and Dockerized development.

## Features

- Register patients with name, email, phone, and document photo
- Pydantic validation
- Stores data in PostgreSQL
- Async confirmation email (Mailtrap)
- Dockerized for easy setup
- Ready for future SMS notification support

## Setup

1. **Clone the repo**

2. **Set Mailtrap credentials**  
   Replace `your_mailtrap_user` and `your_mailtrap_pass` in `docker-compose.yml` with your Mailtrap credentials.

3. **Start the app**
   ```bash
   docker-compose up --build
   ```

4. **API Docs**  
   Visit [http://localhost:8000/docs](http://localhost:8000/docs)

## Endpoints

- `POST /patients`  
  Form-data: name, email, phone, document_photo (file)

- `GET /`  
  Health check

## Testing

You can use the provided `test_main.http` or Swagger UI.

## Notes

- Uploaded files are stored in `app/uploads/`.
- Email is sent asynchronously using Mailtrap.
- SMS notification support can be added in the future.


