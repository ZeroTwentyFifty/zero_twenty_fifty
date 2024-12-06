def test_openid_configuration(client):
    response = client.get("/.well-known/openid-configuration")
    assert response.status_code == 200
    config = response.json()
    assert config["issuer"] == "https://id.example.org"
    assert "token_endpoint" in config