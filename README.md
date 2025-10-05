# BR Trains v2
A UK Train Set addon (newGRF) for OpenTTD, aiming to replicate UK rail (train and tram) rolling stock from the entire history of the British Railway Network

With a focus on real-world consists and liveries, this set is unashamedly real-world-first with an aim to be able to recreate the UK rail network in game. If it's ever run on the UK network, we probably either have it or intend to soon. If you find something missing you love, let us know in Discord on TT-Forums - requests tend to jump to the top of the queue

### Installation
Grab the latest release from the in-game content downloader.

Alternatively get it from the releases page and copy it into your `OpenTTD/newGRF` folder (usually in your Documents folder)

### Building from Source
Easy version: Just push the source to Github and it will build automatically. Otherwise:

Building from the source should be mostly automated using the `build.py` script, but it has a few requirements:
  - Python3.8 (may work on earlier versions but untested)
  - `nml` Python package (available through `pip`)
  
To build the grf completely, just run the following command in your terminal:
```bash
python build.py brtrainsv2
```
This should first compile the `.nml` file, then compile that through to a `.grf` file using `nml`.  Install in the same manner
as previously described, copying the generated `.grf` file into `OpenTTD/newGRF`.


Note, this method still requires the `nml` python package to be installed.

### Credits and Contributions
BRTrains V2 largely Authored/Drawn/Curated by Audigex, built on the work of many others including predecessor projects

This project is a culmination of work by many members of the OpenTTD community over a long period of time

Individual contributions can be found at [CREDITS](./CREDITS.md)

### Contributing
If you want to add to the pack, just pull request it and it might make it in, or join us on Discord (invite link below) and post any sprites you'd like to contribute

### Discord and Forums
- Suggestions, bugs, feedback etc is always welcome on our Discord: https://discord.gg/xWrUDReJdV
- Request and bug reports can also be directed to [our development thread on TT-Forums](https://www.tt-forums.net/viewtopic.php?t=74766)
- Release information (dates, version numbers etc) can be found on [this forum thread](https://www.tt-forums.net/viewtopic.php?t=90160&start=20)

### License
This project is licensed under the GPLv2 license
See [LICENSE](./LICENSE) for license details
