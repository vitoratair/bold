from rest_framework import permissions
from core import constants as c


class InternalRequestPermission(permissions.BasePermission):
    """
        Set permission only to internal requests.
    """

    def _permission_user_agent(self, user_agent):
        """Must check if the user_agent is the internal user_agent configurable."""

        if c.INTERNAL_HTTP_USER_AGENT == user_agent:
            return True

        return False

    def has_permission(self, request):
        """Must check all META data from request to check if the request is a internal request."""

        if not self._permission_user_agent(request.META['HTTP_USER_AGENT']):
            return False

        return True
