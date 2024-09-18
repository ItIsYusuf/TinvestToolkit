from src.application import services

class Services:
    security: services.SecurityService

def client_stocks_service():
    return Services.client_stocks

def security_service():
    return Services.security

def stock_service():
    return Services.stock_service

def upd_stock_service():
    return Services.upd_stock_service