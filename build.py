from pathlib import Path
from sys import argv
from argparse import ArgumentParser
from importlib import util

def append_file(filepath: Path, nml_file: str):
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


def find_files_in_directory(src_directory: Path, filetype: str):
    print("Finding ." + filetype + " files in %s" % src_directory)
    file_list = dict()
    # Iterate through all files in src_directory recursively, finding any that end in .pnml
    for path in src_directory.rglob("*." + filetype):

        # TODO: remove this once handled elsewhhere
        # Don't add the special ones
        #if path.stem in ["railtypes", "grf", "sounds", "templates_shared", "templates_trains", "templates_trams"]:

        if path.parent.stem not in file_list.keys():
            file_list[path.parent.stem] = list()
        file_list[path.parent.stem].append(path)

    # List found files
    for directory in file_list.keys():
        print("Found in directory [%s]:" % directory)
        print([str(file.stem + file.suffix) for file in file_list[directory]])

    return file_list

def handle_folder(directory: Path, filetype: str):
    file_list = dict()

    file_list += find_files_in_directory(directory / "prepend", filetype)

    file_list += find_files_in_directory(directory, filetype)

    file_list += find_files_in_directory(directory / "append", filetype)

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
        # Add lang directory to the build parameters
        parameters = ["--lang", str(lang_dir), "build/" + grf_name + ".nml"]        

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
        return -1

def main(grf_name, src_dir, lang_dir, gfx_dir, b_compile_grf, b_run_game):

    # List of files that have already been added
    processed_files = dict()

    src_directory_name = "src"
    lang_directory_name = "lang"
    gfx_directory_name = "gfx"

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

    # Add the special files to the internal nml file
    nml_file = append_file(src_directory.joinpath("grf." + filetype), nml_file)
    nml_file = append_file(src_directory.joinpath("railtypes." + filetype), nml_file)
    # Sounds, templates should now be handled in /prepend folders

    # Get a list of all the pnml files in src
    file_list = find_files_in_directory(src_directory, filetype)
    print("Finished finding pnml files\n")
    # pushpull_files = list()
    # priority_files = list()
    pnml_files = list()
    # append_files = list()


    # Priority folders: Read all the files in folders that begin with "_" into the internal nml
    #for directory in file_list:
        # Group pushpull files
        # if directory.startswith("PushPull"): 
        #     pushpull_files += file_list[directory]
        #     continue

        # Grab priority files that need to be run first
        # if directory.startswith("_"):
        #     priority_files += file_list[directory]
        #     continue

        # Grab "append" files (that go at the end)
        # if directory == "append":
        #     append_files += file_list[directory]
        #     continue
        
        # Everything else
        # else:
        #         pnml_files += file_list[directory]       

    # pnml_files += file_list[directory]        

    # Special pushpull file first
    # for file in sorted(pushpull_files):
    #     if file.stem.startswith("PushPull"):
    #         print("Found PushPull.pnml special item")
    #         nml_file = append_file(file, nml_file)

    # Read the other pushpull files
    # for file in sorted(pushpull_files):
    #     if file.stem.startswith("PushPull"):
    #         continue;
    #     print("Reading pushpull file '%s'" % (file.stem + file.suffix))
    #     nml_file = append_file(file, nml_file)

    # Read the priority files
    # for file in sorted(priority_files):
    #     print("Reading priority file '%s'" % (file.stem + file.suffix))
    #     nml_file = append_file(file, nml_file)

    # Read the regular files
    for file in sorted(pnml_files):
        # print("Reading '%s'" % (file.stem + file.suffix))
        nml_file = append_file(file, nml_file)

    # Read the append files (mostly switches to disable units)
    # for file in sorted(append_files):
    #     # print("Reading '%s'" % (file.stem + file.suffix))
    #     nml_file = append_file(file, nml_file)

    print("Copied all files to internal buffer\n")

    # Try to write the internal nml to a file
    if write_file(grf_name, nml_file) != 0:
        print("The nml file failed to compile")
        return -1

    # If we're compiling or running the game
    if b_compile_grf:
        # Try to compile the GRF
        error = compile_grf(has_lang_dir, grf_name, lang_dir)
        if error == -1:
            return -2

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
    elif error_code == 1:
        print("The grf file was compiled successfully")
    else:
        print("The nml file was compiled successfully (this is the not grf)")
