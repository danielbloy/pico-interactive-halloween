# pico-interactive-halloween

Moved from https://github.com/danielbloy/pico-interactive/halloween/2024

TODO: Note that each Pico node needs a `settings.toml` file that contains:

```
WIFI_SSID = "<WIFI>"
WIFI_PASSWORD = "Password"
```

* TODO: Note about RAM limitations in Pico devices, particularly with Network and sound being the main hogs
* TODO: Note had to use two devices anyway
* TODO: Note the bodge about not being able to use directory service due to memory
* TODO: Note about Pico running on Laptop for TV and Projector.
* TODO: Note about experimental support for Raspberry Pi (3A+ and Zero 2W)
* TODO: Note about an required upgrade to the power distribution to use normal 13 Amp cable
  and local USB connectors rather than just running 5v 2A so more power can be provided
* TODO: Audio quality using PWM and filter is not fantastic, witch to I2S or 3A+

## Power distribution

In 2023, all nodes (apart from the coordinator) were battery powered. This
offered great flexibility as to positioning but required a lot of batteries
and meant the whole system could not easily be turned off (or on) with a
single switch. For 2024, I am looking for more mains powered distribution.

## New nodes

* Spiders - This is something that was prototyped for 2023 but we ran out
  of time to implement. In essence, a node controls LEDs that are drilled
  into the eyes of some spiders and made to pulse on command. There was also
  some chittering noises. We plan to arrange the spiders in webs over a small
  greenhouse frame. We also have a massive spider to add to the middle :).
  This probably needs 1 or 2 of the new style nodes.
* Thunder and lightning - This can be a repurposed 2023 style node connected
  to a large NeoPixel ring and a set of PC speakers (rather than the in-built
  40mm speakers) to add nice thunder and lightning. It can be triggered
  randomly or via the coordinator node.

## Replaced nodes

* Path - Both the left and right path nodes were fragile and the wireless
  communications introduced tiny delays that were noticeable when trying to
  sync their actions. These two nodes will use 6 separate rings of NeoPixels
  each (1 per skull) rather than one single chain of NeoPixels to control
  chained to the 6 skulls. The communication between the nodes will be direct
  (likely over UART cable but possibly Wi-Fi) to remove delay. The nodes
  will not need to communicate via the coordinator as they will each have
  an ultrasonic sensor so become largely autonomous.

## Upgraded nodes

* Witch - This will have a smoke machine with ice added to the cauldron to
  give a more realistic effect. We will also be adding a second node to allow
  concurrent multiple sounds (the bubbling cauldron and a witch). We will also
  be adding a life-sized witch (actually a skeleton wearing a witches outfit).
  The additional node can be a repurposed 2023 style node. We may also replace
  the lights under the cauldron with NeoPixels controlled by the second node.
  Ideally, the second node will be a 2024 style node with a sensor but time
  to make that node could be an issue.

## Original nodes

* Creepy head - This is actually a MakeCode Arcade based board with screens
  so a completely different kind of node. It'll likely stay the same unless I
  have enough time to get it off the breadboard and soldered together properly.
  It does have a second Pico based board that drives the speaker in the head
  but it just plays a background sound on repeat.

## Future nodes

* Pixie jars - Small jars that contain a Pico with a small Display to animate
  pixies caught in the jar. also this could do blinking eyes like the MakeCode
  Arcade type device.

## License

All materials provided in this project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0
International License. To view a copy of this license, visit
<https://creativecommons.org/licenses/by-nc-sa/4.0/>.

In summary, this means that you are free to:

* **Share** — copy and redistribute the material in any medium or format.
* **Adapt** — remix, transform, and build upon the material.

Provided you follow these terms:

* **Attribution** — You must give appropriate credit , provide a link to the license, and indicate if changes were made.
  You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
* **NonCommercial** — You may not use the material for commercial purposes.
* **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the
  same license as the original.
