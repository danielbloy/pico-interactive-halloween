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
    # These triggers fire on a continuous basis, never stopping.

    def schedule_continuous_trigger(node: str, duration: int):
        async def trigger() -> None:
            asyncio.create_task(trigger_node(node))

        runner.add_task(
            new_scheduled_task(
                trigger,
                frequency=1 / duration,
            ))


    for n, duration in [(EYES, 80), (ROAR, 20)]:
        schedule_continuous_trigger(n, duration)

    ################################
    # N E T W O R K    T R I G G E R
    ################################

    network_trigger_events = TriggerTimedEvents()
    network_trigger_events.add_event(00.00, ZONE_1)
    network_trigger_events.add_event(00.00, ZONE_2)
    network_trigger_events.add_event(00.80, ZONE_3)


    async def start_display() -> None:
        info("Start display")
        network_trigger_events.start()


    async def run_display() -> None:
        events = network_trigger_events.run()

        for event in events:
            if event.event >= len(zone_triggers):
                critical(f"Unknown zone: {event.event}")
                continue

            zone_triggers[event.event].triggered = True


    async def stop_display() -> None:
        info(f"Stop display")
        network_trigger_events.stop()


    def network_trigger() -> None:
        zone_triggers[ZONE_1].triggered = True
        zone_triggers[ZONE_2].triggered = True
        zone_triggers[ZONE_3].triggered = True
        # TODO: Move this to use its own trigger so we can delay the start of each phase.


    server = new_server()
    network_controller = NetworkController(server, network_trigger)
    network_controller.register(runner)

    ############################
    # Z O N E    T R I G G E R S
    ############################

    # Each zone has its own trigger URL that allows then to be independently
    # controlled by different sensors.

    ZONE_1 = 0
    ZONE_2 = 1
    ZONE_3 = 2
    zones = [ZONE_1, ZONE_2, ZONE_3]

    zone_events = [
        TriggerTimedEvents(),
        TriggerTimedEvents(),
        TriggerTimedEvents(),
    ]

    zone_events[ZONE_1].add_event(00.00, PATH_EVENT)
    zone_events[ZONE_1].add_event(00.00, PROJECTOR_EVENT)
    zone_events[ZONE_1].add_event(00.80, WITCH_HOUSE_EVENT_1)
    zone_events[ZONE_1].add_event(00.90, WITCH_HOUSE_EVENT_2)
    zone_events[ZONE_1].add_event(01.00, FIRE_EVENT)
    zone_events[ZONE_1].add_event(01.10, CAULDRON_EVENT)
    zone_events[ZONE_1].add_event(01.20, WITCH_EVENT)
    zone_events[ZONE_1].add_event(02.00, GRAVEYARD_EVENT)


    def create_zone_start(zone: int):
        async def start_display() -> None:
            info(f"Start display for zone {zone + 1}")
            zone_events[zone].start()

        return start_display


    def create_zone_run(zone: int):
        async def run_display() -> None:
            events = zone_events[zone].run()

            tasks = []
            for event in events:
                if event.event >= len(event_to_node):
                    critical(f"Unknown event: {event.event}")
                    continue

                tasks.append(asyncio.create_task(trigger_node(event_to_node[event.event])))

        return run_display


    def create_zone_stop(zone: int):
        async def stop_display() -> None:
            info(f"Stop display for zone {zone + 1}")
            zone_events[zone].stop()

        return stop_display


    zone_triggers = [
        Triggerable(),
        Triggerable(),
        Triggerable(),
    ]

    for zone in zones:
        trigger_loop = new_triggered_task(
            zone_triggers[zone],
            duration=TRIGGER_DURATION,
            start=create_zone_start(zone),
            run=create_zone_run(zone),
            stop=create_zone_stop(zone))
        runner.add_task(trigger_loop)


    def create_zone_trigger(zone: int):
        def trigger(request: Request):
            if request.method == GET:
                zone_triggers[zone].triggered = True
                return Response(request, f"TRIGGERED {zone + 1}")

            return Response(request, "NO", status=NOT_FOUND_404)

        return trigger


    routes = [
        Route("/trigger_1", GET, create_zone_trigger(ZONE_1), append_slash=True),
        Route("/trigger_2", GET, create_zone_trigger(ZONE_2), append_slash=True),
        Route("/trigger_3", GET, create_zone_trigger(ZONE_3), append_slash=True),
    ]
    server.add_routes(routes)

    runner.run()
