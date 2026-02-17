from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address


def test_rate_limit_not_exceeded(client: TestClient) -> None:
    for _ in range(5):
        response = client.get("/api/v1/health")
        assert response.status_code == 200


def test_rate_limit_exceeded() -> None:
    """Test rate limiting with a minimal app that has a very low limit."""
    test_limiter = Limiter(key_func=get_remote_address)
    test_app = FastAPI()
    test_app.state.limiter = test_limiter
    test_app.add_exception_handler(
        RateLimitExceeded, _rate_limit_exceeded_handler
    )
    test_app.add_middleware(SlowAPIMiddleware)

    @test_app.get("/limited")
    @test_limiter.limit("2/minute")
    def limited_endpoint(request: Request) -> dict[str, str]:
        return {"status": "ok"}

    with TestClient(test_app) as c:
        responses = [c.get("/limited").status_code for _ in range(5)]

    assert responses[0] == 200
    assert responses[1] == 200
    assert 429 in responses[2:]
