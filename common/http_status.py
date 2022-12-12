from rest_framework import status

status_types = {
    status.HTTP_200_OK: "Ok",
    status.HTTP_400_BAD_REQUEST: "Bad Request",
    status.HTTP_401_UNAUTHORIZED: "Unauthorised",
    status.HTTP_500_INTERNAL_SERVER_ERROR: "Server Error",
}
