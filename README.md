# pico-interactive-halloween

Please see my website [Code Club Adventures](http://codeclubadventures.com/) for more coding materials.

This project has been moved from https://github.com/danielbloy/pico-interactive/halloween/2024

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
library is available at [pico-interactive](https://github.com/danielbloy/pico-interactive).

The result of the changes during 2024 was this project which contains all the code
and 3D printer files required to build to run the installation. The ambition is
for the installation to be different each year but to provide all the assets here,
along with videos of the finished and working installation.

These video don't quite do it justice but its good enough to get an idea
of what the finished projects look like.

Halloween 2025 [notes](./2025.md), no video yet,

Halloween 2024 [notes](./2024.md), [video on YouTube](https://youtu.be/h3QauCqTOTw)

Halloween 2023 [video on YouTube](https://youtu.be/a0I0U5x334Y), the full code for Halloween 2023 can be
found at https://github.com/danielbloy/pico-interactive-origins.

## Implementation details

Each Pico node running CircuitPython and that is connected to wifi needs a
`settings.toml` file that contains:

```
WIFI_SSID = "<WIFI>"
WIFI_PASSWORD = "Password"
```

Please be aware that there ae some inconsistencies about where settings are stored.
This is in part due to the age differences of some of the materials as well as well
as "how quickly" others have had to be put together. Therefore there is some
inconsistency as some properties are in `config.py` whilst others are in the code files
themselves. It's usually obvious where the settings are or need to be.

# Structure of the code

Code/nodes that need to run on desktop computers such as Raspberry Pis or laptops can
be found in the desktop directory. Code that is designed to run microcontroller based
nodes can be found in microcontroller.

## How to run the code

For all code that is designed to run on a Raspberry Pi Pico, ensure that the device
is running CircuitPython and has [pico-interactive](https://github.com/danielbloy/pico-interactive) copied into the root
of the
device.

For execution on a Desktop computer, the easiest way to execute the code is by using a
Python virtual environment (either from the command-line or via PyCharm). In both
instances, the virtual environment will need to have the `requirements.txt` installed
and a mapping to a copy of pico-interactive](https://github.com/danielbloy/pico-interactive).

If running from PyCharm, setup a virtual environment and add `pico-interactive` as an
additional content root from `File` -> `Settings` -> `Project Structure`.

The following instructions were used to setup such an environment in Ubunutu:

```shell
cd ~/repos
git clone https://github.com/danielbloy/pico-interactive.git
git clone https://github.com/danielbloy/pico-interactive-halloween.git

cd pico-interactive-halloween
python3 -m venv video_venv
source video_venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=~/repos/pico-interactive

cd desktop/video
python main.py
```

On Windows from a command-line, use the following alternative commands:

```shell
cd C:\Workspace\repos
git clone https://github.com/danielbloy/pico-interactive.git
git clone https://github.com/danielbloy/pico-interactive-halloween.git

cd pico-interactive-halloween
python -m venv audio_venv
audio_venv\scripts\activate  
pip install -r requirements.txt
set PYTHONPATH=C:\Workspace\repos\pico-interactive

cd desktop/audio
python main.py
````

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