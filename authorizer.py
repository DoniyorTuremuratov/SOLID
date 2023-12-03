from abc import ABC, abstractmethod

from exceptions import AuthorizationError


class Authorizer(ABC):

    @abstractmethod
    def is_authorized(self) -> bool:
        pass

    def authorize(self):
        if not self.is_authorized():
            raise AuthorizationError("Not authorized")


class SMSAuthorizer(Authorizer):
    def __init__(self):
        self.authorized = False

    def verify_mfa_code(self, code: int) -> None:
        print(f'Verifying SMS code: {code}')
        self.authorized = True

    def is_authorized(self) -> bool:
        return self.authorized


class GoogleAuthorizer(Authorizer):
    def __init__(self):
        self.authorized = False

    def verify_mfa_code(self, code: int) -> None:
        print(f'Verifying Google auth code: {code}')
        self.authorized = True

    def is_authorized(self) -> bool:
        return self.authorized


class RobotAuthorizer(Authorizer):
    def __init__(self):
        self.authorized = False

    def not_a_robot(self):
        self.authorized = True

    def is_authorized(self) -> bool:
        return self.authorized
