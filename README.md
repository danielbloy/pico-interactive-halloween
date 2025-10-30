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

These videos don't quite do it justice but its good enough to get an idea
of what the finished projects look like.

Halloween 2025 [notes](./2025.md), [pictures](2025/overview.md), no video yet,

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

## Structure of the code

Code/nodes that need to run on desktop computers such as Raspberry Pis or laptops can
be found in the desktop directory. Code that is designed to run microcontroller based
nodes can be found in microcontroller.

## How to run the code

For all code that is designed to run on a Raspberry Pi Pico, ensure that the device
is running CircuitPython and has
[pico-interactive](https://github.com/danielbloy/pico-interactive) copied into the
root of the device.

For execution on a Desktop computer, the easiest way to execute the code is by using a
Python virtual environment (either from the command-line or via PyCharm). In both
instances, the virtual environment will need to have the `requirements.txt` installed
and a mapping to a copy of [pico-interactive](https://github.com/danielbloy/pico-interactive).

If running from PyCharm, setup a virtual environment and add `pico-interactive` as an
additional content root from `File` -> `Settings` -> `Project Structure`.

The following instructions were used to setup such an environment in Ubuntu:

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

cd desktop\audio
python main.py
```

### Specific node running instructions

#### Coordinator, back bedroom, Acer Ubuntu laptop

It is easiest to run the Python code using PyCharm.

Because the coordinator node periodically sends trigger messages to the Dragon
node, if the Dragon node is not running, there will be errors reported in the
coordinator nodes console output. This is fine and will not affect the running
operation of the node. Similarly, if any of the other nodes are missing, when
the coordinator node triggers, errors will be reported for each node that is not
online. Again, this is fine.

The coordinator node needs one copy of `pico-interactive-halloween` and one
copy of `pico-interactive`.

Open the `pico-interactive-halloween` project in PyCharm and create a new
a virtual environment if one does not already exist; `File` -> `Settings`
-> `Python` -> `Interpreter`. Remeber to install the `requirements.txt`

Then add `pico-interactive` as an additional content root from `File` ->
`Settings` -> `Project Structure`.

### Projector, lounge, Lenovo Windows laptop

It is easiest to run the Python code using PyCharm.

The Lenovo laptop is a Windows based laptop that runs the video in the lounge.
The easiest way to set this up is to follow the same instructions as for the
Acer Ubuntu laptop that is running the coordinator code.

Replace the contents of `desktop\video\config.py` with those from
`desktop\video\projector_config.py`.

Copy the videos that are to be played into `\desktop\video`.

#### Dragon, bedroom, Medion Windows laptop

This is run on the Medion laptop which runs Windows. It needs one copy of
`pico-interactive-halloween` and two copies of `pico-interactive`. One copy
of `pico-interactive` should be vanilla whilst the second copy should have
the variable `NETWORK_PORT_DESKTOP` changed from 5001 to 5002 in the file
`interactive/control.py`. This is because we run two python scripts as the
on the machine, one for the eyes (video) and one for the roaring (audio).

Replace the contents of `desktop\video\config.py` with those from
`desktop\video\eyes_config.py`.

Copy the videos that are to be played into `\desktop\video`.

The audio files are stored alongside the source code so do not need copying.

On Windows from two command-line windows, use the following commands to
execute the audio and video programs on the Dragon node (make sure
`pico-interactive2` has the configuration changed to be on port 5002 rather
than 5001):

```shell
cd C:\Workspace\repos\pico-interactive-halloween
audio_venv\scripts\activate  
set PYTHONPATH=C:\Workspace\repos\pico-interactive2
cd desktop\audio
python main.py
````

```shell
cd C:\Workspace\repos\pico-interactive-halloween
video_venv\scripts\activate  
set PYTHONPATH=C:\Workspace\repos\pico-interactive
cd desktop\video
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