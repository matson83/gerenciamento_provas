import json
import pytest
from django.contrib.auth import get_user_model
from ninja_jwt.tokens import RefreshToken

User = get_user_model()

@pytest.fixture
def admin_user(db):
    return User.objects.create_user(
        username='admin_teste',
        password='admin123',
        email='admin@teste.com',
        role='ADMIN'
    )

@pytest.fixture
def admin_token(admin_user):
    refresh = RefreshToken.for_user(admin_user)
    return str(refresh.access_token)

@pytest.mark.django_db
def test_login_admin(client, admin_user):
    response = client.post(
        "/api/auth/login",
        data=json.dumps({"username": "admin_teste", "password": "admin123"}),
        content_type="application/json"
    )
    assert response.status_code == 200
    assert "access" in response.json()

@pytest.mark.django_db
def test_registro_admin(client):
    response = client.post(
        "/api/auth/registro",
        data=json.dumps({
            "username": "novo_admin",
            "password": "senha123",
            "email": "novo@admin.com",
            "role": "ADMIN"
        }),
        content_type="application/json"
    )
    assert response.status_code == 200
    assert response.json()["user"]["role"] == "ADMIN"

@pytest.mark.django_db
def test_acesso_admin(client, admin_token):
    response = client.get(
        "/api/admin/dashboard",
        HTTP_AUTHORIZATION=f"Bearer {admin_token}"
    )
    assert response.status_code == 200
    assert "Bem-vindo Admin" in response.json()["message"]