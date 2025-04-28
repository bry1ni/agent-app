# Agent App API Documentation

This document provides detailed information about the Agent App API endpoints.

## Base URL

All API endpoints are prefixed with `/v1`.

## Authentication

Currently, the API does not require authentication. This may change in future versions.

## Endpoints

### Answer a Query

`POST /v1/answer`

Answers a given query using the agent system.

#### Request Body

```json
{
    "query": "string"
}
```

#### Response

```json
{
    "answer": "string"
}
```

#### Example

```bash
curl -X POST "http://localhost:8000/v1/answer" \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the capital of France?"}'
```

#### Response Codes

- `200`: Success
- `500`: Internal server error

### Test Endpoint

`GET /v1/test`

A simple test endpoint to verify the API is running.

#### Response

```json
{
    "message": "Hello, World!"
}
```

#### Example

```bash
curl "http://localhost:8000/v1/test"
```

#### Response Codes

- `200`: Success

## Error Handling

All endpoints may return the following error responses:

### 500 Internal Server Error

```json
{
    "detail": "Error message describing what went wrong"
}
```

## Rate Limiting

Currently, there are no rate limits implemented. This may change in future versions.

## Versioning

The API is versioned through the URL path (e.g., `/v1/...`). Future versions will maintain backward compatibility where possible.

## Best Practices

1. Always include the `Content-Type: application/json` header for POST requests
2. Handle all possible error responses in your client code
3. Implement retry logic for failed requests
4. Cache responses when appropriate to reduce server load 