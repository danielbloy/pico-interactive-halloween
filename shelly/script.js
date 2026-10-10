// MAC address of your Shelly BLU Motion (lowercase)
let TARGET_BLU_MAC = "b0:c7:de:7f:09:18";
// The HTTP endpoint you want to trigger
let WEBHOOK_URL = "http://192.168.1.175/trigger";

Shelly.addEventHandler(function (event) {
    print("DEBUG EVENT RECEIVED: ", JSON.stringify(status));
    // Check if event is from a BTHome component / Bluetooth device
    if (event.component && event.component.indexOf("bthome") === 0) {
        let data = event.info;

        // Look for motion/person detection event
        // Note: Shelly BLU Motion sends motion/presence flags via BTHome
        if (data && data.addr && data.addr.toLowerCase() === TARGET_BLU_MAC) {
            if (data.motion === true || data.sen === true) {
                print("Motion detected by BLU Motion! Calling HTTP endpoint...");

                Shelly.call(
                    "HTTP.GET",
                    {url: WEBHOOK_URL},
                    function (response, error_code, error_message) {
                        if (error_code === 0) {
                            print("HTTP request successful: " + response.body);
                        } else {
                            print("HTTP request failed: " + error_message);
                        }
                    }
                );
            }
        }
    }
});

let MOTION_COMPONENT_ID = "bthomesensor:200";
let WEBHOOK_URL = "http://192.168.1.175/trigger";

print("Script started. Monitoring " + MOTION_COMPONENT_ID + "...");

Shelly.addStatusHandler(function (status) {
    // Check if the change event belongs to our motion sensor component
    print("DEBUG STATUS RECEIVED: ", JSON.stringify(status));
    if (status.component === MOTION_COMPONENT_ID) {

        // Look strictly for the 'value' change inside the status update
        if (typeof status.delta.value !== "undefined") {
            let isMotion = status.delta.value;

            // If motion is detected (true or 1)
            if (isMotion) {
                print("Person detected! Triggering local endpoint...");

                Shelly.call(
                    "HTTP.GET",
                    {url: WEBHOOK_URL, timeout: 5},
                    function (response, error_code, error_message) {
                        if (error_code === 0) {
                            print("Webhook successful! Code: " + response.code);
                        } else {
                            print("Webhook error: " + error_message);
                        }
                    }
                );
            }
        }
    }
});