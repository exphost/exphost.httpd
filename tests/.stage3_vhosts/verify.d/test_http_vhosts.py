def test_http_static_vhost1(host):
    response = host.check_output("curl 127.0.0.1:8084/content.txt -H 'Host: test-vhost1.example.com'")
    assert response == "http_app_1"

def test_http_php_vhost1(host):
    response = host.check_output("curl 127.0.0.1:8084/sum.php -H 'Host: test-vhost1.example.com'")
    assert response == "1+1=2"

def test_http_static_vhost2(host):
    response = host.check_output("curl 127.0.0.1:8084/content.txt -H 'Host: test-vhost2.example.com'")
    assert response == "http_app_2"
    response = host.check_output("curl 127.0.0.1:8084/content.txt -H 'Host: test-vhost2.example.pl'")
    assert response == "http_app_2"

def test_http_php_vhost2(host):
    response = host.check_output("curl 127.0.0.1:8084/sum.php -H 'Host: test-vhost2.example.com'")
    assert response == "2+2=4"
    response = host.check_output("curl 127.0.0.1:8084/sum.php -H 'Host: test-vhost2.example.pl'")
    assert response == "2+2=4"

def test_http_static_vhost3(host):
    response = host.check_output("curl 127.0.0.1:8085/content.txt")
    assert response == "http_app_3"

def test_http_php_vhost3(host):
    response = host.check_output("curl 127.0.0.1:8085/sum.php")
    assert response == "3+3=6"

def test_http_rewrite_vhost4(host):
    assert host.check_output("curl http://127.0.0.1:8084/wp -H 'Host: test-vhost4.example.com' -I -w '%{redirect_url}' -s -o /dev/null") == "https://wp.pl"
    assert host.check_output("curl http://127.0.0.1:8084/onet -H 'Host: test-vhost4.example.com' -I -w '%{redirect_url}' -s -o /dev/null") == "https://onet.pl"

def test_http_directory_vhost4(host):
    host.ansible(
        "shell",
        r"mkdir -p /app/httpd/httpd/var/www/test-vhost4/path1 && echo test_file1 > /app/httpd/httpd/var/www/test-vhost4/path1/file.txt",
        become=True,
        become_user='httpd',
        check=False)
    host.ansible(
        "shell",
        r"mkdir -p /srv/http/test && echo test_file2 > /srv/http/test/file.txt && chcon -t httpd_sys_rw_content_t /srv/http -R",
        become=True,
        check=False)
    assert host.check_output("curl -H 'Host: test-vhost4.example.com' http://127.0.0.1:8084/path1/file.txt") == "test_file1"
    assert host.check_output("curl -H 'Host: test-vhost4.example.com' http://127.0.0.1:8084/path2/file.txt") == "test_file2"

def test_http_basic_auth_vhost5(host):
    response = host.check_output("curl 127.0.0.1:8085/content.txt -H 'Host: test-vhost5.example.com' -o /dev/null -w '%{http_code}' -s")
    assert response == "401"

    response = host.check_output("curl 127.0.0.1:8085/content.txt -H 'Host: test-vhost5.example.com' -o /dev/null -w '%{http_code}' -s -u u1:password1")
    assert response == "200"
    response = host.check_output("curl 127.0.0.1:8085/content.txt -H 'Host: test-vhost5.example.com' -o /dev/null -w '%{http_code}' -s -u u2:password2")
    assert response == "200"
    response = host.check_output("curl 127.0.0.1:8085/content.txt -H 'Host: test-vhost5.example.com' -o /dev/null -w '%{http_code}' -s -u u3:password3")
    assert response == "401"

    response = host.check_output("curl 127.0.0.1:8085/content.txt -H 'Host: test-vhost5.example.com' -s -u u1:password1")
    assert response == "http_app_1"
