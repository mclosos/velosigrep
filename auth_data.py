# а почему байт строки?
HOSTS = {"184.253.11.40": ["admin",b"Ft6gGT"], "localhost":["adm", b"1234"]}


def auth_data(ip_addr):
    """
    Abstract function which return login and password
    """
    return HOSTS[ip_addr]
