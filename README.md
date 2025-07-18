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
   Please have in mind the Docker service should be active.
   
5. **API Docs**  
   Visit [http://localhost:8000/docs](http://localhost:8000/docs)

## Endpoints

#### `POST /patients`  
Creates a new patient.

**cURL example:**
```bash
curl --location 'http://localhost:8000/patients' \
--header 'Cookie: jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY4NWVkNGE3MTVkNGU1YjI0MzBmZGIyZSIsImlhdCI6MTc1MjQ2MjM3NiwiZXhwIjoxNzUyNDY1OTc2fQ.Zmb56iXQBn8ia8v09Fyty7ELVlPMANaE0J84a_7ZNTw' \
--form 'name="Facundo Carrizo"' \
--form 'email="facundocarrizo99@gmail.com"' \
--form 'phone="1134031128"' \
--form 'document_photo=@"/Users/facundocarrizo/Pictures/my-notion-face-portrait.png"' 
```
  

#### `GET /`  
Health check

**cURL example:**
```bash
curl --location 'http://localhost:8000/' \
--header 'Cookie: jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY4NWVkNGE3MTVkNGU1YjI0MzBmZGIyZSIsImlhdCI6MTc1MjQ2MjM3NiwiZXhwIjoxNzUyNDY1OTc2fQ.Zmb56iXQBn8ia8v09Fyty7ELVlPMANaE0J84a_7ZNTw'
```

## Testing

You can use the provided `test_main.http`

## Notes

- Uploaded files are stored in `app/uploads/`.
- Email is sent asynchronously using Mailtrap.
- SMS notification support can be added in the future.

Evidence of data being saved on PostgreSQL:

<img width="1429" height="448" alt="image" src="https://github.com/user-attachments/assets/60462fe4-6699-4680-a11d-4215f3090674" />

Evidence of Service running on Docker:

<img width="1222" height="448" alt="image" src="https://github.com/user-attachments/assets/cf7552ab-d5f9-4a2a-8e3d-0bab9992f48c" />

Evidence of Mail being sent:

<img width="1289" height="332" alt="image" src="https://github.com/user-attachments/assets/09cf99a2-eae9-428a-9b8b-bccaf7b07b68" />
