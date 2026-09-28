Traceback (most recent call last):
  File "C:\Users\AROBLEDO\AppData\Local\Programs\Python\Python313\Lib\site-packages\urllib3\connectionpool.py", line 464, in _make_request
    self._validate_conn(conn)
    ~~~~~~~~~~~~~~~~~~~^^^^^^
  File "C:\Users\AROBLEDO\AppData\Local\Programs\Python\Python313\Lib\site-packages\urllib3\connectionpool.py", line 1093, in _validate_conn
    conn.connect()
    ~~~~~~~~~~~~^^
  File "C:\Users\AROBLEDO\AppData\Local\Programs\Python\Python313\Lib\site-packages\urllib3\connection.py", line 741, in connect
    sock_and_verified = _ssl_wrap_socket_and_match_hostname(
        sock=sock,
    ...<14 lines>...
        assert_fingerprint=self.assert_fingerprint,
    )
  File "C:\Users\AROBLEDO\AppData\Local\Programs\Python\Python313\Lib\site-packages\urllib3\connection.py", line 920, in _ssl_wrap_socket_and_match_hostname
    ssl_sock = ssl_wrap_socket(
        sock=sock,
    ...<8 lines>...
        tls_in_tls=tls_in_tls,
    )
  File "C:\Users\AROBLEDO\AppData\Local\Programs\Python\Python313\Lib\site-packages\urllib3\util\ssl_.py", line 480, in ssl_wrap_socket
    ssl_sock = _ssl_wrap_socket_impl(sock, context, tls_in_tls, server_hostname)
  File "C:\Users\AROBLEDO\AppData\Local\Programs\Python\Python313\Lib\site-packages\urllib3\util\ssl_.py", line 524, in _ssl_wrap_socket_impl
    return ssl_context.wrap_socket(sock, server_hostname=server_hostname)
           ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\AROBLEDO\AppData\Local\Programs\Python\Python313\Lib\ssl.py", line 455, in wrap_socket
    return self.sslsocket_class._create(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        sock=sock,
        ^^^^^^^^^^
    ...<5 lines>...
        session=session
        ^^^^^^^^^^^^^^^
    )
    ^
  File "C:\Users\AROBLEDO\AppData\Local\Programs\Python\Python313\Lib\ssl.py", line 1076, in _create
    self.do_handshake()
    ~~~~~~~~~~~~~~~~~^^
  File "C:\Users\AROBLEDO\AppData\Local\Programs\Python\Python313\Lib\ssl.py", line 1372, in do_handshake
    self._sslobj.do_handshake()
    ~~~~~~~~~~~~~~~~~~~~~~~~~^^
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate (_ssl.c:1028)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\AROBLEDO\AppData\Local\Programs\Python\Python313\Lib\site-packages\urllib3\connectionpool.py", line 787, in urlopen
    response = self._make_request(
        conn,
    ...<10 lines>...
        **response_kw,
    )
  File "C:\Users\AROBLEDO\AppData\Local\Programs\Python\Python313\Lib\site-packages\urllib3\connectionpool.py", line 488, in _make_request
    raise new_e
urllib3.exceptions.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate (_ssl.c:1028)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Users\AROBLEDO\AppData\Local\Programs\Python\Python313\Lib\site-packages\requests\adapters.py", line 667, in send
    resp = conn.urlopen(
        method=request.method,
    ...<9 lines>...
        chunked=chunked,
    )
  File "C:\Users\AROBLEDO\AppData\Local\Programs\Python\Python313\Lib\site-packages\urllib3\connectionpool.py", line 841, in urlopen
    retries = retries.increment(
        method, url, error=new_e, _pool=self, _stacktrace=sys.exc_info()[2]
    )
  File "C:\Users\AROBLEDO\AppData\Local\Programs\Python\Python313\Lib\site-packages\urllib3\util\retry.py", line 519, in increment
    raise MaxRetryError(_pool, url, reason) from reason  # type: ignore[arg-type]
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='localhost', port=65002): Max retries exceeded with url: /api/consultores (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate (_ssl.c:1028)')))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "c:\Users\AROBLEDO\source\repos\CommanCenter.API\scripts\cargue_prueba.py", line 122, in <module>
    main()
    ~~~~^^
  File "c:\Users\AROBLEDO\source\repos\CommanCenter.API\scripts\cargue_prueba.py", line 113, in main
    r = s.post(API_URL + CONSULTORES_PATH, json=payload, timeout=60)
  File "C:\Users\AROBLEDO\AppData\Local\Programs\Python\Python313\Lib\site-packages\requests\sessions.py", line 637, in post
    return self.request("POST", url, data=data, json=json, **kwargs)
           ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\AROBLEDO\AppData\Local\Programs\Python\Python313\Lib\site-packages\requests\sessions.py", line 589, in request
    resp = self.send(prep, **send_kwargs)
  File "C:\Users\AROBLEDO\AppData\Local\Programs\Python\Python313\Lib\site-packages\requests\sessions.py", line 703, in send
    r = adapter.send(request, **kwargs)
  File "C:\Users\AROBLEDO\AppData\Local\Programs\Python\Python313\Lib\site-packages\requests\adapters.py", line 698, in send
    raise SSLError(e, request=request)
requests.exceptions.SSLError: HTTPSConnectionPool(host='localhost', port=65002): Max retries exceeded with url: /api/consultores (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate (_ssl.c:1028)')))
