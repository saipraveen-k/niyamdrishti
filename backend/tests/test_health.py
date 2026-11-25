"""
Smoke tests: health check and root endpoints.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "NiyamDrishti API"
    assert "docs" in data
    assert "health" in data


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["app"] == "NiyamDrishti"
    assert "env" in data
    assert "ai_available" in data


@pytest.mark.asyncio
async def test_health_env_is_development(client: AsyncClient):
    """In tests the env should always be 'development'."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["env"] == "development"


@pytest.mark.asyncio
async def test_openapi_schema_accessible(client: AsyncClient):
    """OpenAPI schema should be accessible in non-production mode."""
    response = await client.get("/api/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "paths" in data


@pytest.mark.asyncio
async def test_unknown_route_returns_404(client: AsyncClient):
    response = await client.get("/nonexistent-path-xyz")
    assert response.status_code == 404
