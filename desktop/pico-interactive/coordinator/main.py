# This is designed to run on a desktop computer and perform the multi-node coordination.
#
# The Eyes are displayed on the TV on the 1st floor and are kicked off on repeat
# even when the trigger is not activated. The eyes act as an attract to the house.
#

import asyncio

from adafruit_httpserver import Route, GET, Response, \
    Request, NOT_FOUND_404

from interactive.log import critical
from interactive.log import info
from interactive.network import NetworkController, send_message
from interactive.polyfills.network import new_server
from interactive.runner import Runner
from interactive.scheduler import new_triggered_task, Triggerable, TriggerTimedEvents, \
    new_scheduled_task
from nodes import *

# The main display length (apart from the projector which will be longer in many cases).
TRIGGER_DURATION = 45

# Events
PATH_EVENT = 0
WITCH_HOUSE_EVENT_1 = 1
WITCH_HOUSE_EVENT_2 = 2
CAULDRON_EVENT = 3
FIRE_EVENT = 4
WITCH_EVENT = 5
GRAVEYARD_EVENT = 6
PROJECTOR_EVENT = 7

event_to_node = [
    PATH,
    WITCH_HOUSE_1,
    WITCH_HOUSE_2,
    CAULDRON,
    FIRE,
    WITCH,
    GRAVEYARD,
    PROJECTOR
]

if __name__ == '__main__':

    runner = Runner()

    runner.cancel_on_exception = False
    runner.restart_on_exception = True
    runner.restart_on_completion = False


    async def trigger_node(node: str) -> None:
        """
        Sends a trigger message to the desired node.
        """
        info(f"Triggering {node}")

        debug = True
        if debug:
            print(f"DEBUG sending trigger message to {node}")
        else:
            send_message("trigger", host=node)


    ####################################
    # C O N S T A N T    T R I G G E R S
    ####################################
    def schedule(node: str, duration: int):
        async def trigger() -> None:
            asyncio.create_task(trigger_node(node))

        runner.add_task(
            new_scheduled_task(
                trigger,
                frequency=1 / duration,
            ))


    for n, duration in [(EYES, 80), (ROAR, 20)]:
        schedule(n, duration)

    ZONE_1 = 0
    ZONE_2 = 1
    ZONE_3 = 2

    trigger_events = [
        TriggerTimedEvents(),
        TriggerTimedEvents(),
        TriggerTimedEvents(),
    ]
    trigger_events[ZONE_1].add_event(00.00, PATH_EVENT)
    trigger_events[ZONE_1].add_event(00.00, PROJECTOR_EVENT)
    trigger_events[ZONE_1].add_event(00.80, WITCH_HOUSE_EVENT_1)
    trigger_events[ZONE_1].add_event(00.90, WITCH_HOUSE_EVENT_2)
    trigger_events[ZONE_1].add_event(01.00, FIRE_EVENT)
    trigger_events[ZONE_1].add_event(01.10, CAULDRON_EVENT)
    trigger_events[ZONE_1].add_event(01.20, WITCH_EVENT)
    trigger_events[ZONE_1].add_event(02.00, GRAVEYARD_EVENT)


    def get_zone_start(zone: int):
        async def start_display() -> None:
            info(f"Start display for zone {zone + 1}")
            trigger_events[zone].start()

        return start_display


    def get_zone_run(zone: int):
        async def run_display() -> None:
            events = trigger_events[zone].run()

            tasks = []
            for event in events:
                if event.event >= len(event_to_node):
                    critical(f"Unknown event: {event.event}")
                    continue

                tasks.append(asyncio.create_task(trigger_node(event_to_node[event.event])))

        return run_display


    def get_zone_stop(zone: int):
        async def stop_display() -> None:
            info(f"Stop display for zone {zone + 1}")
            trigger_events[zone].stop()

        return stop_display


    triggerable = [
        Triggerable(),
        Triggerable(),
        Triggerable(),
    ]

    for zone in range(3):
        trigger_loop = new_triggered_task(
            triggerable[zone],
            duration=TRIGGER_DURATION,
            start=get_zone_start(zone),
            run=get_zone_run(zone),
            stop=get_zone_stop(zone))
        runner.add_task(trigger_loop)


    def network_trigger() -> None:
        triggerable[ZONE_1].triggered = True
        triggerable[ZONE_2].triggered = True
        triggerable[ZONE_3].triggered = True
        # TODO: Move this to use its own trigger so we can delay the start of each phase.


    server = new_server()
    network_controller = NetworkController(server, network_trigger)
    network_controller.register(runner)


    def get_network_zone_trigger(zone: int):
        def trigger(request: Request):
            if request.method == GET:
                triggerable[zone].triggered = True
                return Response(request, f"TRIGGERED {zone + 1}")

            return Response(request, "NO", status=NOT_FOUND_404)

        return trigger


    routes = [
        Route("/trigger_1", GET, get_network_zone_trigger(ZONE_1), append_slash=True),
        Route("/trigger_2", GET, get_network_zone_trigger(ZONE_2), append_slash=True),
        Route("/trigger_3", GET, get_network_zone_trigger(ZONE_3), append_slash=True),
    ]
    server.add_routes(routes)

    runner.run()
