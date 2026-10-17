# This is a simple `cptkip` app that can be run on a desktop or microcontroller to
# validate that messages are being received from the Shelly sensors with each sensor
# being a trigger.
import cptkip.config.configuration as config
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
    <title>CPTKIP</title>
</head>
<body>
<p>Hello from the <strong>CPTKIP HTTP Server!</strong></p>
</body>
</html>
"""

duration = 10

if hasattr(config, "TRIGGER_DURATION"):
    duration = config.TRIGGER_DURATION

info(f"TRIGGER_DURATION: {duration}")

triggers = [False, False, False]


def begin_display(trigger: int) -> None:
    # TODO: LEDs
    info(f"Start {trigger + 1}")


def end_display(trigger: int) -> None:
    # TODO: LEDs
    info(f"Stop {trigger + 1}")


def create_trigger_task(trigger: int) -> Callable[[], bool]:
    return create_triggered_task(
        lambda: triggers[trigger],
        duration=duration,
        begin=lambda: begin_display(trigger),
        end=lambda: end_display(trigger))


def clear_trigger() -> bool:
    global triggers
    triggers = [False, False, False]
    return True


server = Server()


@server.route("/", "GET")
def main(query_parameters, headers, body):
    return Response(__INDEX_HTML, content_type="text/html")


@server.route("/index.html", "GET")
def main(query_parameters, headers, body):
    return Response(__INDEX_HTML, content_type="text/html")


@server.route("/trigger_1", "GET")
def main(query_parameters, headers, body):
    triggers[0] = True
    return Response("TRIGGERED 1", content_type="text/plain")


@server.route("/trigger_2", "GET")
def main(query_parameters, headers, body):
    triggers[1] = True
    return Response("TRIGGERED 2", content_type="text/plain")


@server.route("/trigger_3", "GET")
def main(query_parameters, headers, body):
    triggers[2] = True
    return Response("TRIGGERED 3", content_type="text/plain")


listen = server.create_task()

functions = [listen]
for i, _ in enumerate(triggers):
    functions.append(create_trigger_task(i))

functions.append(clear_trigger)

if hasattr(config, "REPORT_RAM") and config.REPORT_RAM:
    monitor = memory_monitor_task.create(4, 1, lambda: True)
    functions.append(monitor)

# noinspection broad-exception
try:
    run(*functions)
except:
    if not is_running_on_desktop():
        import microcontroller

        microcontroller.reset()
