# 🏦 Currency Convertor API

![Docker Pulls](https://img.shields.io/docker/pulls/deyrahul95/currency-convertor) 
![Python Version](https://img.shields.io/badge/python-3.13-blue)
![CI](https://github.com/deyrahul95/CurrencyConvertor/actions/workflows/docker-release.yml/badge.svg)


A lightweight Docker image for a **currency conversion API** built with FastAPI. Convert amounts between different currencies using predefined exchange rates.  

---

## Features

- Simple REST API to convert currencies.
- Predefined exchange rates (can be extended in the code).
- Built with **FastAPI** and ready to run in Docker.
- Lightweight and easy to deploy.

---

## Usage

### Pull the image

```bash
docker pull deyrahul95/currency-convertor:latest
```

### Run the container

```bash
docker run -d --rm \
  --name currency-convertor-app \
  -p 8000:8000 \
  deyrahul95/currency-convertor:latest
```

## Test the API

Once the container is running, you can use curl or a browser to test the /convert endpoint.

### Example:

```bash
curl "http://localhost:8000/convert?from_currency=USD&to_currency=EUR&amount=100"
```

### Sample Response

```bash
{
  "amount": "100",
  "result": "92.40",
  "rate": "0.92"
}
```