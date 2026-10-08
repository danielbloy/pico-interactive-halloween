from cptkip.core.control import SEND_MESSAGE_TIMEOUT
from cptkip.core.environment import is_running_on_desktop
from cptkip.network.biplane import Server, Response
from cptkip.network.requests import requests
from cptkip.task import memory_monitor_task
from cptkip.task.basic_runner import run

# collections.abc is not available in CircuitPython.
if is_running_on_desktop():
    from collections.abc import Callable


def __add_routes(server: Server):
    @server.route("/hi", "GET")
    def main(query_parameters, headers, body):
        return Response("<b>hi!</b>", content_type="text/html")


HEADER_NAME = 'name'  # Name of the sender.
HEADER_ROLE = 'role'  # Role of the sender.

HEADERS = {
    HEADER_NAME: "configuration.NODE_NAME",  # TODO: This should come from configuration
    HEADER_ROLE: "configuration.NODE_ROLE",  # TODO: This should come from configuration
}


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

    __add_routes(server)
    listen = server.create_task()

    # TODO: Get monitor settings from configuration
    monitor = memory_monitor_task.create(4, 1, lambda: True)

    run(*funcs, listen, monitor)
