def test_http_static(host):
    response = host.check_output("curl 127.0.0.1:8083/content.txt -H 'Host: test-php.example.com'")
    assert response == "http_app_1"

def test_http_php(host):
    response = host.check_output("curl 127.0.0.1:8083/sum.php -H 'Host: test-php.example.com'")
    assert response == "1+1=2"
