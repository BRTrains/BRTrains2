# ModernUKTrainset
A Modern UK Train Set for OpenTTD, designed to be played alongside BRTrains.

### Train List
|Completed|Planned|
|:-:|:-:|
|Class 195 (2-Car)|Class 68|
|Class 195 (3-Car)|CLass 397|
||Class 769|
||Class 707|
||Class 717|
||Class 745|
||Class 755|
||Class 777|
||Class 800/0|
||Class 800/1|
||Class 800/2|
||Class 800/3|

### Installation
Grab the latest release from the releases page, put in your OpenTTD/newGRF folder, then add to the game using newGRF settings.

### Building from Source
Building from the source should be mostly automated using the `build.py` script, but it has a few requirements:
  - Python3.8 (may work on earlier versions but untested)
  - `nml` Python package (available through `pip`)
  
To build the the grf completely, just run the folllowing command in your terminal of choice:
```bash
python3 build.py --compile mukts
```
This should first compile the `.nml` file, then compile that through to a `.grf` file using `nml`.  Install in the same manner
as previously described, copying the generated `.grf` file into `OpenTTD/newGRF`.

### Adding Content to the Pack
If you want to add to the pack, just pull request it and it might make it in.  
Alternatively, if you just want to steal the build script then go wild.
