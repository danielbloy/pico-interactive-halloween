import cptkip.config.configuration as config
from cptkip.core.control import SEND_MESSAGE_TIMEOUT
from cptkip.core.environment import is_running_on_desktop
from cptkip.network.biplane import Server, Response
from cptkip.network.requests import requests
from cptkip.task import memory_monitor_task
from cptkip.task.basic_runner import run

# collections.abc is not available in CircuitPython.
if is_running_on_desktop():
    from collections.abc import Callable

__INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pico Interactive</title>
</head>
<body>
<p>Hello from the <strong>CircuitPython HTTP Server!</strong></p>
</body>
</html>
"""

NO = "NO"
YES = "YES"
OK = "OK"
ON = "ON"
OFF = "OFF"

TRIGGERED = "TRIGGERED"
HEADER_NAME = 'name'  # Name of the sender.
HEADER_ROLE = 'role'  # Role of the sender.

NODE_NAME = "unknown"
NODE_ROLE = "unknown"
if hasattr(config, "NODE_NAME"):
    NODE_NAME = config.NODE_NAME

if hasattr(config, "NODE_ROLE"):
    NODE_NAME = config.NODE_ROLE

HEADERS = {
    HEADER_NAME: NODE_NAME,
    HEADER_ROLE: NODE_ROLE,
}


def __add_routes(server: Server, trigger: Callable[[], None]):
    """
    Defines the routes supported by the server. This is a subset of those defined in
    pico-interactive but includes support for the crucial trigger event which calls
    the passed in trigger function.
    """

    @server.route("/", "GET")
    def main(query_parameters, headers, body):
        return Response(__INDEX_HTML, content_type="text/html", headers=HEADERS)

    @server.route("/index.html", "GET")
    def main(query_parameters, headers, body):
        return Response(__INDEX_HTML, content_type="text/html", headers=HEADERS)

    @server.route("/restart", "GET")
    def main(query_parameters, headers, body):
        if is_running_on_desktop():
            return Response(NO, content_type="text/plain", headers=HEADERS)

        import microcontroller
        microcontroller.reset()

        return Response(YES, content_type="text/plain", headers=HEADERS)

    @server.route("/alive", "GET")
    def main(query_parameters, headers, body):
        return Response(YES, content_type="text/plain", headers=HEADERS)

    @server.route("/name", "GET")
    def main(query_parameters, headers, body):
        return Response(NODE_NAME, content_type="text/plain", headers=HEADERS)

    @server.route("/role", "GET")
    def main(query_parameters, headers, body):
        return Response(NODE_ROLE, content_type="text/plain", headers=HEADERS)

    @server.route("/trigger", "GET")
    def main(query_parameters, headers, body):
        trigger()
        return Response(TRIGGERED, content_type="text/plain", headers=HEADERS)


def send_message(path: str, host: str,
                 protocol: str = "http", method="GET",
                 data=None, json=None):
    """
    Sends a message with the provided payload to the specified node, ensuring headers are included.
    """
    return requests.request(method, f"{protocol}://{host}/{path}",
                            headers=HEADERS, data=data, json=json,
                            timeout=SEND_MESSAGE_TIMEOUT)


def execute(trigger: Callable[[], None], *funcs: Callable[[], bool]):
    """
    Executes the network code whilst also running the supplied tasks. A callback can be
    provided that is called when the network code receives a trigger message.
    """
    server = Server()

    __add_routes(server, trigger)
    listen = server.create_task()
    functions = [*funcs, listen]

    if hasattr(config, "REPORT_RAM") and config.REPORT_RAM:
        monitor = memory_monitor_task.create(4, 1, lambda: True)
        functions.append(monitor)

    run(*functions)
