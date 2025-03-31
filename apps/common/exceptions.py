from rest_framework.views import exception_handler
from rest_framework.exceptions import ErrorDetail


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(response.data, dict) and all(
            key in response.data for key in ("status", "code", "message", "errors")
        ):
            return response

        error_message = []
        error_details = []

        if isinstance(response.data, dict):
            if "detail" in response.data:
                # Simple error (permission denied, etc.)
                error_message = str(response.data["detail"])
                error_details = str(response.data["detail"])

            else:
                # Field-specific validation errors
                for field, errors in response.data.items():
                    if isinstance(errors, list):
                        clean_errors = [
                            err if isinstance(err, str) else str(err) for err in errors
                        ]
                        error_message.append(f"{field}: {', '.join(clean_errors)}")
                        error_details.append(f"{field}: {', '.join(clean_errors)}")
                    else:
                        error_message.append(f"{field}: {errors}")
                        error_details.append(f"{field}: {errors}")

                error_message = " ".join(error_message)
                error_details = " ".join(error_details)

        response.data = {
            "status": "error",
            "code": response.status_code,
            "message": error_message if error_message else "Invalid request",
            "errors": {
                "details": error_details if error_details else "Validation failed"
            },
        }

    return response
