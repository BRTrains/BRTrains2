# ModernUKTrainset
A UK Train Set for OpenTTD including all the latest British Rail classes to be introduced between 2015 and 2020. This set is designed to be played with BRTrains (BRTrains lacks classes from between 2015 and 2020, so this newGRF completes the gap) rather than on its own. Graphics are designed to work best with the Finescale UK Track Set, but will work with any track combination.

### Train List
|Completed|In Progress|Planned|
|:-:|:-:|:-:|
|Class 195/0/1||Class 68|
|Class 331/0/1||Class 397|
|Class 800/0/1/2/3||Class 769|
|Class 801/1/2||Class 707|
|Class 802/0/1/2/3||Class 717|
|||Class 745|
|||Class 755|
|||Class 777|

### Installation
Grab the latest release from the releases page, put in your OpenTTD/newGRF folder, then add to the game using newGRF settings.

### Building from Source
Building from the source should be mostly automated using the `build.py` script, but it has a few requirements:
  - Python3.8 (may work on earlier versions but untested)
  - `nml` Python package (available through `pip`)
  
To build the grf completely, just run the following command in your terminal:
```bash
python3 build.py --compile mukts
```
This should first compile the `.nml` file, then compile that through to a `.grf` file using `nml`.  Install in the same manner
as previously described, copying the generated `.grf` file into `OpenTTD/newGRF`.

To copy the grf and start the game, closing all existing instances, run the following command in your terminal:
```bash
python3 build.py --run mukts
```
This will also perform the --compile function before starting the game.

### Adding Content to the Pack
If you want to add to the pack, just pull request it and it might make it in.  
Alternatively, if you just want to steal the build script then go wild.
