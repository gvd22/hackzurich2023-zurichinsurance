# Backend
## Deploy

### Local

Run app with `uvicorn main:app --reload --host 0.0.0.0`.

### Docker image 
```
docker build -t backend .
docker run -p80:80 --rm backend
```

## Inference
Test the api using following curl command in the terminal:
```
curl --location --request GET 'http://localhost:8000/insurances'
```