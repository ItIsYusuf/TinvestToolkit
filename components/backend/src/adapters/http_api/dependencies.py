from src.application import services

class Services:
    security: services.SecurityService


def security_service():
    return Services.security