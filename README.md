# BR Trains v2
A UK Train Set for OpenTTD, based on the original BRTrains set (itself based on the unfinished BRSet and BROS, previous attempts at a UK set) and Modern UK Train Set (MUTS), an independent add-on for BRTrains including trains released after 2015 (the last date available in BRTrains v1)

This set aims to combine the BRTrains and MUTS sets, and add modern liveries to trains originally included in BRTrains, and fix colouring/scaling and other graphical inconsistencies in the BRTrains set, since that set was developed by many users over many years and is not known for excessive consistency...

### Train List


### Installation
Grab the latest release from the in-game content downloader.

Alternatively get it from the releases page and copy it into your `OpenTTD/newGRF` folder.

### Building from Source
Easy version: Just push the source to Github and it will build automatically. Otherwise:

Building from the source should be mostly automated using the `build.py` script, but it has a few requirements:
  - Python3.8 (may work on earlier versions but untested)
  - `nml` Python package (available through `pip`)
  
To build the grf completely, just run the following command in your terminal:
```bash
python build.py --compile brtrainsv2
```
This should first compile the `.nml` file, then compile that through to a `.grf` file using `nml`.  Install in the same manner
as previously described, copying the generated `.grf` file into `OpenTTD/newGRF`.

To copy the grf and start the game, closing all existing instances, run the following command in your terminal of choice:
```bash
python build.py --run brtrainsv2
```
This will also perform the --compile function, and will not start the game if an error is thrown during the compilation process.

#### Building with Powershell
Alternatively, you can build the project through Powershell.
To find out how to use the Powershell build script, simply run:
```powershell
Get-Help .\build.ps1 -Full
```
The most commonly used command invocation is:
```powershell
.\build.ps1 -StartGame -Verbose
```
Note, this method still requires the `nml` python package to be installed.

### Credits (in no particular order)

#### Developers

- Audigex - BRTrains v2 (This project)
- Leander - BRTrains
- Gwyd - BRTrains
- KubaP - MUTS  
- AlmostCthulhu - MUTS   

#### Artists

- Leander  
- Ameecher  
- Voyager One  
- Class93  
- RailwayMan  
- KubaP  
- AlmostCthuluhu  
- Audigex  
- Gwyd  
- Ronstar  
- Purno  
- le_harv  
- Helmar  
- Pilot  
- Growl  
- Red Dragon  
- Beardie  
- TheAmir259  
- GamingBloke  
- SquireJames  
- Erato  
- DJ Nekkid 
- Welshdragon
- Doorslammer
- AndyTheNorth
- Su1phur

... And other BROS artists who's names have been lost along the way

Detailed BROS credits available at https://docs.google.com/spreadsheets/d/1XVF7VXa1B5tcqJiXRvRNtJ34bvyPZL9UtzXi1YENuts/edit#gid=1244600467


### Contributing
If you want to add to the pack, just pull request it and it might make it in, or join us on Discord (invite link below) and post any sprites you'd like to contribute

### Discord

Suggestions, bugs, feedback etc is always welcome on our Discord: https://discord.gg/xWrUDReJdV

### License
This project is licensed under the GPLv2 license
See [LICENSE](./LICENSE) for license details
