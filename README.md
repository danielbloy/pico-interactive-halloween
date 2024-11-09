# pico-interactive-halloween

Moved from https://github.com/danielbloy/pico-interactive/halloween/2024

My daughter loves Halloween and after Halloween 2022 (she was 8 years old at the
time) we discussed using some of the electronics that I use in my Coding Clubs to
make our house more interactive with sounds and lights. I agreed to this because
how hard could it possibly be? Well it turns out it was a massive undertaking and
very stressful! But she loved it and that was all that mattered.

Once over, we decided to go bigger for 2024 and fix a number of the issues we had
with the 2023 setup. As I knew it'd be a bunch of work I started earlier (March
2024). It was still really difficult to get it all done on time but did look even
more impressive. Yes, she was happy again! The work done for 2024 was implemented
in a fashion to make it generic and reusable for lots of projects. The full
library is available at https://github.com/danielbloy/pico-interactive.

For 2025 we are going bigger again. Yes, I'm starting even earlier. Janaury! The
main change here is to hardwire as much as possible to make the entire house look
like a single installation that works together. It'll be awesome.

These video don't quite do it justice but its good enough to get an idea
of what the finished projects look like.

Halloween 2023 [video on YouTube](https://youtu.be/a0I0U5x334Y)

Halloween 2024 [video on YouTube](https://youtu.be/h3QauCqTOTw)

## Halloween 2023

The full code for Halloween 2023 can be found at https://github.com/danielbloy/pico-interactive-origins.

## Halloween 2024

### Power distribution

In 2023, all nodes (apart from the coordinator) were battery powered. This
offered great flexibility as to positioning but required a lot of batteries
and meant the whole system could not easily be turned off (or on) with a
single switch. For 2024, I am looking for more mains powered distribution.

### New nodes

**Sensors**
Separate boxes for sensors to make the entire system automatic. It mostly worked.

**Spiders**

This is something that was prototyped for 2023 but we ran out
  of time to implement. In essence, a node controled LEDs that are drilled
  into the eyes of some spiders and made to pulse on command. However, the
  final implementation reused a lot of parts from the 2023 path nodes and
  used NeoPixels and a 3D printed holder that projected eyes and lines onto
  glow-in-the-dark spiders. It was very effective.

**Projector**

This was really easy to add and very effective.

**TV**

This was used as an attract with blinking eyes. Very easy to add and very
effective.

**Thunder and lightning**

This was integrated into the spiders node to save
  time. That was a mistake due to power draw.

### Replaced nodes

**Path**

Both the left and right path nodes were fragile and the wireless
  communications introduced tiny delays that were noticeable when trying to
  sync their actions. These two nodes will use 6 separate rings of NeoPixels
  each (1 per skull) rather than one single chain of NeoPixels to control
  chained to the 6 skulls. The communication between the nodes will be direct
  (likely over UART cable but possibly Wi-Fi) to remove delay. The nodes
  will not need to communicate via the coordinator as they will each have
  an ultrasonic sensor so become largely autonomous.

### Upgraded nodes

**Witch**

This had an atomiser added to the cauldron to give a more realistic effect.
It reused 3 of the 2023 boxes for multiple sounds; though the 2023 boxes are
much quieter than the 2024 boxes.

We will also added a life-sized witch (actually a mannequin wearing a witches
outfit).
  
### Original nodes

**Creepy head**

This is actually a MakeCode Arcade based board with screens so a completely different
kind of node. It does have a second Pico based board that drives the speaker in the
head but it just plays a background sound on repeat.

## Halloween 2025

Key planned changes:

* Remove more wi-fi, using hardcoded cables instead
* Better sensor/trigger system. Fwer false positives and quicker to act.
* More waterproofing and bigger boxes to hold electronis
* Smoke machine
* Another projector
* More power Pico 2 microcontrollers and introduction of Rasberry Pi Zero 2/3 computers
* Even better power distribution
* Move to high quality audio using separate controllers or I2S.
* Larger powered speakers
* Coffin that shakes and makes noises
* Boxs that opens with eyes
* Moving spiders
* Multiple separate thunder and lightning boxes to make the effect isntallation
  wide rather than just in the spider enclosure


## Implementation details

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
* TODO: Audio quality using PWM and filter is not fantastic, switch to I2S or 3A+
  TODO: Note the inconsistency that some properties are in `config.py` whilst others are in the code file.

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
