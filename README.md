# pico-interactive-halloween

Please see my website [Code Club Adventures](http://codeclubadventures.com/) for more coding materials.

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

For 2025 we are going bigger again. Yes, I'm starting even earlier. January! The
main change here is to hardwire as much as possible to make the entire house look
like a single installation that works together. It'll be awesome.

These video don't quite do it justice but its good enough to get an idea
of what the finished projects look like.

Halloween 2023 [video on YouTube](https://youtu.be/a0I0U5x334Y)

Halloween 2024 [video on YouTube](https://youtu.be/h3QauCqTOTw)

## Implementation details

TODO: Note that each Pico node needs a `settings.toml` file that contains:

```python
WIFI_SSID = "<WIFI>"
WIFI_PASSWORD = "Password"
```

Please be aware that there ae some inconsistencies about where settings are stored. This is in part
due to the age differences of some of the materials as well as well as "how quickly" others have
had to be put together. Therefore there is some inconsistency as some properties are in `config.py`
whilst others are in the code files themselves. It's usually obvious where the settings are or need
to be.

## Halloween 2025

Both the 2023 and 2024 displays took a massive amount of time to design and build. This was
in part because I was learning what worked and what didn't as I wen't along as well as building
everything from scratch. The amount of time invested was also so significant that it made it
very difficult to progress other projects that I'm working on. So for 2025, I'm focussing on
using what I already have and turning that into a more coherent display. Crucially, part of the
display will be covered to protect it from the elements and this opens it up to much more
impressive display possibilities. It also means my daughter can take a larger part in designing
and building the project; particularly the witches house.

Also, as I've learnt so much about what dorks and what doesn't, I'm designing all-new control
boxes and a completely new software stack using everything I've learnt so far. Unlike previous
years I'm not rushing to put them into production. Rather I will be working on the boxes, the
software stack and the new circuit boards over 2025 and through into 2026 with a view to replace
the older 2023 boxes first. If you are interested, the new software stack can be found at
[cptkip](https://github.com/danielbloy/cptkip).

Key planned changes for 2025:

* Improve the TV and projector code to work with Raspberry Pis.
* Re-arrange outdoors so the left-hand side of the house is the graveyard.
* Re-arrange outdoors so the right-hand side of the house is a covered witches house.
* Add a smoke machine.

## Halloween 2024

### Power distribution

In 2023, all nodes (apart from the coordinator) were battery powered. This
offered great flexibility as to positioning but required a lot of batteries
and meant the whole system could not easily be turned off (or on) with a
single switch. For 2024, I am looking for more mains powered distribution.

### New nodes

#### Sensors

Separate boxes for sensors to make the entire system automatic. It mostly worked.

#### Spiders

This is something that was prototyped for 2023 but we ran out
of time to implement. In essence, a node controlled LEDs that are drilled
into the eyes of some spiders and made to pulse on command. However, the
final implementation reused a lot of parts from the 2023 path nodes and
used NeoPixels and a 3D printed holder that projected eyes and lines onto
glow-in-the-dark spiders. It was very effective.

#### Projector

This was really easy to add and very effective.

#### TV

This was used as an attract with blinking eyes. Very easy to add and very
effective.

#### Thunder and lightning

This was integrated into the spiders node to save
time. That was a mistake due to power draw.

### Replaced nodes

#### Path

Both the left and right path nodes were fragile and the wireless
communications introduced tiny delays that were noticeable when trying to
sync their actions. These two nodes will use 6 separate rings of NeoPixels
each (1 per skull) rather than one single chain of NeoPixels to control
chained to the 6 skulls. The communication between the nodes will be direct
(likely over UART cable but possibly Wi-Fi) to remove delay. The nodes
will not need to communicate via the coordinator as they will each have
an ultrasonic sensor so become largely autonomous.

### Upgraded nodes

#### Witch

This had an atomiser added to the cauldron to give a more realistic effect.
It reused 3 of the 2023 boxes for multiple sounds; though the 2023 boxes are
much quieter than the 2024 boxes.

We will also added a life-sized witch (actually a mannequin wearing a witches
outfit).
  
### Original nodes

#### Creepy head

This is actually a MakeCode Arcade based board with screens so a completely different
kind of node. It does have a second Pico based board that drives the speaker in the
head but it just plays a background sound on repeat.

## Halloween 2023

The full code for Halloween 2023 can be found at https://github.com/danielbloy/pico-interactive-origins.

## Roadmap

These are some of the things I'd like to do over the coming years.

* Re-build the creepy head so it is an actual head.
* Boxes that opens with eyes
* Remove more wi-fi, using hardcoded cables instead to Picos instead due to the range and reliability of the pico wi-fi
* Use Raspberry Pis (probably 3A or 3B) to handle the broader wi-fi connectivity.
* Better sensor/trigger system. Fewer false positives and quicker to act.
* Add another projector
* More powerful Pico 2 microcontrollers and introduction of Raspberry Pi Zero 2/3 computers
* Even better power distribution
* Move to high quality audio using separate controllers or I2S.
* Larger powered speakers
* Coffin that shakes and makes noises
* Moving spiders
* Multiple separate thunder and lightning boxes to make the effect installation
  wide rather than just in the spider enclosure

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
