import cptkip.config.configuration as config
from cptkip.core.control import SEND_MESSAGE_TIMEOUT
from cptkip.core.environment import is_running_on_desktop
from cptkip.core.logging import info
from cptkip.network.biplane import Server, Response
from cptkip.task import memory_monitor_task
from cptkip.task.basic_runner import run
from cptkip.task.triggered_task import create as create_triggered_task

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
    from cptkip.network.requests import requests
    return requests.request(method, f"{protocol}://{host}/{path}",
                            headers=HEADERS, data=data, json=json,
                            timeout=SEND_MESSAGE_TIMEOUT)


def execute(begin_display, run_display, end_display: Callable[[], None],
            *funcs: Callable[[], bool]):
    """
    Executes the network connected display. Three functions must be provided and these
    are passed directly to the triggered task. Other normal runner functions can be
    passed in too and these get executed on each iteration, after any trigger event but
    before the trigger is cleared.
    """

    duration = 40

    if hasattr(config, "TRIGGER_DURATION"):
        duration = config.TRIGGER_DURATION

    info(f"TRIGGER_DURATION: {duration}")

    triggered = False

    triggered_task = create_triggered_task(
        lambda: triggered,
        duration=duration,
        begin=begin_display,
        func=run_display,
        end=end_display,
        continue_func=lambda: True)

    def clear_trigger() -> bool:
        nonlocal triggered
        triggered = False
        return True

    def trigger():
        nonlocal triggered
        triggered = True

    server = Server()
    __add_routes(server, trigger)
    listen = server.create_task()

    # This is not the most Pythonic way to do this but it needs to work with CircuitPython.
    functions = [listen, triggered_task]
    for func in funcs:
        functions.append(func)

    functions.append(clear_trigger)

    if hasattr(config, "REPORT_RAM") and config.REPORT_RAM:
        monitor = memory_monitor_task.create(4, 1, lambda: True)
        functions.append(monitor)

    # noinspection broad-exception
    try:
        # TODO: This currently uses just basic_runner as that is all cktpip currently
        #       provides. When a reliable runner becomes available we should switch to that.
        #       In the mean time, we will simply restart the microcontroller if an exception
        #       is generated.
        run(*functions)
    except:
        if not is_running_on_desktop():
            import microcontroller
            microcontroller.reset()
