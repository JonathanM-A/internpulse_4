# your_app/middleware.py
from django.utils import timezone
from rest_framework.throttling import SimpleRateThrottle


class RateLimitHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Always add headers if throttling is enabled
        if hasattr(request, "throttle_durations"):
            for throttle in request.throttle_durations:
                if isinstance(throttle, SimpleRateThrottle):
                    history = throttle.history
                    if history:
                        response["X-RateLimit-Limit"] = throttle.num_requests
                        remaining = max(0, throttle.num_requests - len(history))
                        response["X-RateLimit-Remaining"] = remaining
                        reset_time = history[-1] + throttle.duration
                        response["X-RateLimit-Reset"] = int(
                            reset_time - timezone.now().timestamp()
                        )
                        break

        # For throttled responses
        if hasattr(request, "throttled"):
            throttle = request.throttled
            response["X-RateLimit-Limit"] = throttle.rate
            response["X-RateLimit-Remaining"] = 0
            response["X-RateLimit-Reset"] = int(throttle.wait)

        print(f"{dict(response.headers)}")

        return response

