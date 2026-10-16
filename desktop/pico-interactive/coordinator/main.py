# This is designed to run on a desktop computer and perform the multi-node coordination.
#
# The Eyes are displayed on the TV on the 1st floor and are kicked off on repeat
# even when the trigger is not activated. The eyes act as an attract to the house.
#

import asyncio

from adafruit_httpserver import Route, GET, Response, \
    Request, NOT_FOUND_404

from interactive.log import critical, debug
from interactive.log import info
from interactive.network import NetworkController, send_message
from interactive.polyfills.network import new_server
from interactive.runner import Runner
from interactive.scheduler import new_triggered_task, Triggerable, TriggerTimedEvents, \
    new_scheduled_task
from nodes import *

DEBUG = True  # TODO: Set to False

# The main display length (apart from the projector which will be longer in many cases)
# and the duration for each of the zones.
DISPLAY_DURATION = 45  # This is 5 seconds longer than the actual display
ZONE_1_DURATION = 45  # This is 5 seconds longer than the actual display
ZONE_2_DURATION = 45  # This is 5 seconds longer than the actual display
ZONE_3_DURATION = 45  # This is 5 seconds longer than the actual display

# TODO: Reduce the witches node to 30 seconds.
# TODO: Rework sounds and timing for the witches nodes.

# Each zone has its own trigger URL that allows it to be independently
# triggered by a different sensor.

ZONE_1 = 0  # Path and graveyard
ZONE_2 = 1  # Front door
ZONE_3 = 2  # Witches house

zones = [ZONE_1, ZONE_2, ZONE_3]

zone_triggers = [
    Triggerable(),
    Triggerable(),
    Triggerable(),
]

zone_durations = [
    ZONE_1_DURATION,
    ZONE_2_DURATION,
    ZONE_3_DURATION,
]

zone_events = [
    TriggerTimedEvents(),
    TriggerTimedEvents(),
    TriggerTimedEvents(),
]

# These constants are indexes into the event_to_path node and used as events
# in the triggers.
PATH_NODE = 0
WITCH_HOUSE_NODE_1 = 1
WITCH_HOUSE_NODE_2 = 2
CAULDRON_NODE = 3
FIRE_NODE = 4
WITCH_NODE = 5
GRAVEYARD_NODE = 6
PROJECTOR_NODE = 7
FRONT_DOOR_NODE = 8

event_to_node = [
    PATH,
    WITCH_HOUSE_1,
    WITCH_HOUSE_2,
    CAULDRON,
    FIRE,
    WITCH,
    GRAVEYARD,
    PROJECTOR,
    FRONT_DOOR
]

zone_events[ZONE_1].add_event(00.00, PATH_NODE)
zone_events[ZONE_1].add_event(00.00, PROJECTOR_NODE)
zone_events[ZONE_1].add_event(02.00, GRAVEYARD_NODE)

zone_events[ZONE_2].add_event(00.00, FRONT_DOOR_NODE)
# TODO: Add in the 3 `cptkip` nodes.

zone_events[ZONE_3].add_event(00.00, WITCH_HOUSE_NODE_1)
zone_events[ZONE_3].add_event(00.00, WITCH_HOUSE_NODE_2)
zone_events[ZONE_3].add_event(00.00, FIRE_NODE)
zone_events[ZONE_3].add_event(00.00, CAULDRON_NODE)
zone_events[ZONE_3].add_event(00.00, WITCH_NODE)

network_trigger = Triggerable()

network_trigger_events = TriggerTimedEvents()
network_trigger_events.add_event(00.00, ZONE_1)
network_trigger_events.add_event(02.00, ZONE_2)
network_trigger_events.add_event(06.00, ZONE_3)

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

        if DEBUG:
            debug(f"Sending trigger message to {node}")
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

    # This is the default trigger for the `pico-interactive` framework. If this
    # is invoked, we trigger each of the zones at the desired interval using the
    # configured events. Each zone is controlled separately with its own event set.

    async def start_display() -> None:
        info("Start display")
        network_trigger_events.start()


    async def run_display() -> None:
        events = network_trigger_events.run()

        for event in events:
            if event.event >= len(zone_triggers):
                critical(f"Unknown zone: {event.event}")
                continue

            print(f"Triggering zone {event}...")
            zone_triggers[event.event].triggered = True


    async def stop_display() -> None:
        info("Stop display")
        network_trigger_events.stop()


    network_trigger_loop = new_triggered_task(
        network_trigger,
        duration=DISPLAY_DURATION,
        start=start_display,
        run=run_display,
        stop=stop_display)
    runner.add_task(network_trigger_loop)


    def trigger() -> None:
        network_trigger.triggered = True


    server = new_server()
    network_controller = NetworkController(server, trigger)
    network_controller.register(runner)


    ############################
    # Z O N E    T R I G G E R S
    ############################

    # Here we configure a triggerable set of events for each zone and setup
    # a specific URL for each. The configuration of the events is specified
    # at the top of this file.

    def create_zone_start(zone: int):
        async def start() -> None:
            info(f"Start display for zone {zone + 1}")
            zone_events[zone].start()

        return start


    def create_zone_run(zone: int):
        async def run() -> None:
            events = zone_events[zone].run()

            tasks = []
            for event in events:
                if event.event >= len(event_to_node):
                    critical(f"Unknown event: {event.event}")
                    continue

                tasks.append(asyncio.create_task(trigger_node(event_to_node[event.event])))

        return run


    def create_zone_stop(zone: int):
        async def stop() -> None:
            info(f"Stop display for zone {zone + 1}")
            zone_events[zone].stop()

        return stop


    for zone in zones:
        trigger_loop = new_triggered_task(
            zone_triggers[zone],
            duration=zone_durations[zone],
            start=create_zone_start(zone),
            run=create_zone_run(zone),
            stop=create_zone_stop(zone))
        runner.add_task(trigger_loop)


    def create_zone_trigger_url(zone: int):
        def trigger(request: Request):
            if request.method == GET:
                zone_triggers[zone].triggered = True
                return Response(request, f"TRIGGERED {zone + 1}")

            return Response(request, "NO", status=NOT_FOUND_404)

        return trigger


    routes = [
        Route("/trigger_1", GET, create_zone_trigger_url(ZONE_1), append_slash=True),
        Route("/trigger_2", GET, create_zone_trigger_url(ZONE_2), append_slash=True),
        Route("/trigger_3", GET, create_zone_trigger_url(ZONE_3), append_slash=True),
    ]
    server.add_routes(routes)

    runner.run()
