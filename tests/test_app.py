from http import HTTPStatus


def test_app_connection(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Manga API esta rodando!'}
