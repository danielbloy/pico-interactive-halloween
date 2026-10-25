# Rename this to code.py on the CircuitPython device.
# This code runs event triggered sounds.
import cptkip.config.configuration as config
from cptkip.core.logging import info
from cptkip.task.triggered_events_task import create, Trigger
from cptkip.zero.audio import create_pwm_queue

queue = create_pwm_queue()


def begin_display() -> None:
    trigger.triggered = True


def run_display() -> None:
    queue.update()


def end_display() -> None:
    queue.cancel()


trigger = Trigger(False)


def queue_sound(file: str) -> None:
    info(f"Queueing sound: {file}")
    queue.queue(file)


events_task = create(trigger, config.EVENTS, callback=queue_sound, continue_func=lambda: True)

from network import execute

execute(begin_display, run_display, end_display, events_task)
