from pathlib import Path
from sys import argv
from argparse import ArgumentParser
from importlib import util


def check_project_structure(src_directory: Path, gfx_directory: Path,
                            lang_directory: Path):

    has_lang_dir = True

    # Check that the project is properly structured
    if not src_directory.exists():
        print("\"src\" directory not found.  Aborting")
        return (False, -1)
    if not gfx_directory.exists():
        print("\"gfx\" directory not found.  Aborting")
        return (False, -1)
    if not lang_directory.exists():
        print(
            "\"lang\" directory not found.  Assuming hard-coded strings (this is not best practice)"
        )
        has_lang_dir = False

    # Find the grf, railtypes, and templates files
    if not src_directory.joinpath("grf.pnml").exists():
        print(
            "\"grf.pnml\" not found.  It should be in \"src\" and contain the grf block"
        )
        return (False, -1)
    if not src_directory.joinpath("railtypes.pnml").exists():
        print(
            "\"railtypes.pnml\" not found.  It should be in \"src\" and contain the railtypetable block"
        )
        return (False, -1)
    if not src_directory.joinpath("sounds.pnml").exists():
        print(
            "\"sounds.pnml\" not found.  Assuming no sounds are required"
        )
    if not src_directory.joinpath("templates_shared.pnml").exists():
        print(
            "\"templates_shared.pnml\" not found.  Assuming no templates are required"
        )
    if not src_directory.joinpath("templates_trains.pnml").exists():
        print(
            "\"templates_trains.pnml\" not found.  Assuming no templates are required"
        )
    if not src_directory.joinpath("templates_trams.pnml").exists():
        print(
            "\"templates_trams.pnml\" not found.  Assuming no templates are required"
        )

    print("Project structure is correct\n")
    return (has_lang_dir, 0)


def copy_file(filepath: Path, nml_file: str):
    # If the pnml filepath doesn't exist, exit
    if not filepath.exists():
        print("The file <%s> does not exist" % str(filepath))
        return -1

    # Read the pnml file into the internal nml
    with open(str(filepath), "r") as file:
        nml_file += "// " + filepath.stem + filepath.suffix + "\n"
        for line in file:
            nml_file += line
    nml_file += "\n\n"
    return nml_file


def find_files(src_directory: Path, filetype: str):
    print("Finding ." + filetype + " files in %s" % src_directory)
    file_list = dict()
    # Iterate through all files in src_directory recursively, finding any that end in .pnml
    for path in src_directory.rglob("*." + filetype):
        # Don't add the special ones
        if path.stem in ["railtypes", "grf", "sounds", "templates_shared", "templates_trains", "templates_trams"]:
            continue

        if path.parent.stem not in file_list.keys():
            file_list[path.parent.stem] = list()
        file_list[path.parent.stem].append(path)

    # List found files
    for directory in file_list.keys():
        print("Found in directory [%s]:" % directory)
        print([str(file.stem + file.suffix) for file in file_list[directory]])

    return file_list


def write_file(filename: str, nml_file: str):
    from os import makedirs
    # Generate the filepath and check if it exists
    filepath = Path("build/" + filename + ".nml")
    build_dir = Path("build/")
    if not build_dir.exists():
        makedirs("build")

    if filepath.exists():
        print("'%s.nml' already exists.  Overwriting" % filename)

    # Write the internal nml to the file
    with open(filepath, "w") as file_writer:
        for line in nml_file:
            file_writer.write(line)

    print("Written all files to '%s.nml' file\n" % filename)
    return 0


def compile_grf(has_lang_dir, grf_name, lang_dir):
    # Check if we have the nml package
    found_nml = util.find_spec("nml")
    if found_nml is not None:
        # Import nml's main module
        import nml.main
        parameters = []
        if has_lang_dir:
            # If we have a lang directory, add it to the parameters
            parameters = ["--lang", str(lang_dir), "build/" + grf_name + ".nml"]
        else:
            # If not, just the nml name
            parameters = ["build/" + grf_name + ".nml"]
        try:
            # Try to compile the nml file
            nml.main.main(parameters)
        except SystemExit:
            # nml uses sys.exit(), so catch this to stop the program exiting
            print("nml tried to exit but was stopped")
        print("Finished compiling grf file\n")
        return 1
    else:
        # nml isn't installed
        print("nml is not installed.  You can get it using 'pip install nml'")
        return -2

def main(grf_name, src_dir, lang_dir, gfx_dir, b_compile_grf, b_run_game):

    # List of files that have already been added
    processed_files = set()

    src_directory_name = "src"
    lang_directory_name = "lang"
    gfx_directory_name = "gfx"

    prepend_directory_name = "prepend"
    append_directory_name = "append"

    sprite_suffix = "sprites"
    switch_suffix = "switches"

    filetype = "pnml"

    src_directory = Path(src_directory_name)
    lang_directory = Path(lang_directory_name)
    gfx_directory = Path(gfx_directory_name)

    # Variant Headers
    variantheader_directory = Path(src_directory_name + "variantheader")

    # Electric
    electric_mu_directory = Path(src_directory_name + "electric_MU")
    electric_loco_directory = Path(src_directory_name + "electric_loco")
    # Diesel
    diesel_mu_directory = Path(src_directory_name + "diesel_MU")
    diesel_loco_directory = Path(src_directory_name + "diesel_loco")
    # Multimode
    multimode_mu_directory = Path(src_directory_name + "multimode_MU")
    multimode_loco_directory = Path(src_directory_name + "multimode_loco")
    # Alternative Fuel (battery, hyrdogen)
    altfuel_mu_directory = Path(src_directory_name + "altfuel_MU")
    altfuel_loco_directory = Path(src_directory_name + "altfuel_loco")
    # Steam
    steam_loco_directory = Path(src_directory_name + "steam_loco")
    # Metro
    metro_directory = Path(src_directory_name + "metro")

    # Rolling Stock
    rolling_stock_directory = Path(src_directory_name + "rolling_stock")
    # Freight
    freight_wagon_directory = Path(src_directory_name + "freight_wagon")
    # Utility and Debug
    utility = Path(src_directory_name + "utility_and_debug")

    nml_file = ""
    has_lang_dir = False

    # Check if the project is set up properly and we have a lang directory
    (has_lang_dir,
     error_code) = check_project_structure(src_directory, gfx_directory,
                                           lang_directory)
    if error_code != 0:
        return -1

    # Add the special files to the internal nml file
    nml_file = copy_file(src_directory.joinpath("grf." + filetype), nml_file)
    nml_file = copy_file(src_directory.joinpath("railtypes." + filetype), nml_file)
    # Sounds, templates should now be handled in /prepend folders
    #nml_file = copy_file(src_directory.joinpath("sounds." + filetype), nml_file)
    #nml_file = copy_file(src_directory.joinpath("templates_shared." + filetype), nml_file)
    #nml_file = copy_file(src_directory.joinpath("templates_trains." + filetype), nml_file)
    #nml_file = copy_file(src_directory.joinpath("templates_trams." + filetype), nml_file)

    # Get a list of all the pnml files in src
    file_list = find_files(src_directory, filetype)
    print("Finished finding pnml files\n")
    pushpull_files = list()
    priority_files = list()
    pnml_files = list()
    append_files = list()
    # Priority folders: Read all the files in folders that begin with "_" into the internal nml
    for directory in file_list:
        # Group pushpull files
        if directory.startswith("PushPull"): 
            pushpull_files += file_list[directory]
            continue

        # Grab priority files that need to be run first
        if directory.startswith("_"):
            priority_files += file_list[directory]
            continue

        # Grab "append" files (that go at the end)
        if directory == "append":
            append_files += file_list[directory]
            continue
        
        # Everything else
        else:
                pnml_files += file_list[directory]             

    # Special pushpull file first
    for file in sorted(pushpull_files):
        if file.stem.startswith("PushPull"):
            print("Found PushPull.pnml special item")
            nml_file = copy_file(file, nml_file)

    # Read the other pushpull files
    for file in sorted(pushpull_files):
        if file.stem.startswith("PushPull"):
            continue;
        print("Reading pushpull file '%s'" % (file.stem + file.suffix))
        nml_file = copy_file(file, nml_file)

    # Read the priority files
    for file in sorted(priority_files):
        print("Reading priority file '%s'" % (file.stem + file.suffix))
        nml_file = copy_file(file, nml_file)

    # Read the regular files
    for file in sorted(pnml_files):
        # print("Reading '%s'" % (file.stem + file.suffix))
        nml_file = copy_file(file, nml_file)

    # Read the append files (mostly switches to disable units)
    for file in sorted(append_files):
        # print("Reading '%s'" % (file.stem + file.suffix))
        nml_file = copy_file(file, nml_file)

    print("Copied all files to internal buffer\n")

    # Try to write the internal nml to a file
    if write_file(grf_name, nml_file) != 0:
        print("The nml file failed to compile")
        return -1

    # If we're compiling or running the game
    if b_compile_grf or b_run_game:
        # Try to compile the GRF
        error = compile_grf(has_lang_dir, grf_name, lang_dir)
        if error == -2:
            return -2
        elif b_run_game == False:
            return 1

    # Optionally run the game
    if b_run_game:
        return run_game(grf_name)

    return 0


if __name__ == "__main__":
    # Parser arguments
    parser = ArgumentParser(description="Compile pnml files into one nml file")
    parser.add_argument("grf_name")
    parser.add_argument("--src", default="src", help="Source files directory")
    parser.add_argument("--lang",
                        default="lang",
                        help="Language files directory")
    parser.add_argument("--gfx",
                        default="gfx",
                        help="Graphics files directory")
    parser.add_argument("--compile",
                        action="store_true",
                        help="Compile the nml file with nmlc")
    parser.add_argument(
        "--run",
        action="store_true",
        help="Run the game after compilation (will also compile the file.  Also kills existing instances)")
    args = parser.parse_args()

    # Reports any errors in the nml file compilation process
    error_code = main(args.grf_name, args.src, args.lang, args.gfx,
                      args.compile, args.run)
    if error_code == -1:
        print(
            "The nml file failed to compile properly.  Please consult the log")
    elif error_code == -2:
        print("The nml file compiled correctly, but nml failed to compile it")
    elif error_code == -3:
        print(
            "The grf file compiled successfully but the game failed to start")
    elif error_code == 1:
        print("The grf file was compiled successfully")
    elif error_code == 2:
        print(
            "The grf file was compiled successfully, and the game was started")
    else:
        print("The nml file was compiled successfully (this is the not grf)")
