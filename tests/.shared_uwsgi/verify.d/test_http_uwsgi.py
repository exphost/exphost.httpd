import http.client
def test_http_django_8081(host):
    response = host.check_output("curl 127.0.0.1:8081/test/ -H 'Host: test-django.example.com'")
    assert response == "Working"

def test_http_django_8082(host):
    response = host.check_output("curl 127.0.0.1:8082/test/ -H 'Host: test-django.example.com'")
    assert response == "Working"
