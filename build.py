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
        nml_file += "// " + str(filepath) + "\n"
        for line in file:
            nml_file += line
    nml_file += "\n\n"
    return nml_file

def find_files_in_directory(src_directory: Path, auto = False):
    print("Finding .pnml files in %s" % src_directory)
    
    search_files = sorted(src_directory.glob("*.pnml"))        

    file_list = dict()
    # Iterate through all files in src_directory, finding any that end in .pnml
    for path in search_files:        
        # Don't add duplicates
        if str(path.parent) not in file_list.keys():
            file_list[str(path.parent)] = list()
        file_list[str(path.parent)].append(path)

    # List found files
    for directory in file_list.keys():
        print("Found in directory [%s]:" % directory)
        print([str(file.stem + file.suffix) for file in file_list[directory]])

    return file_list

def handle_folder(directory: Path, auto=False):
    file_list = dict()

    if not directory.exists():
        print("Cannot handle folder: The path <%s> does not exist" % str(directory))
        return file_list # Return empty dict


    if (directory / "prepend").exists():
        file_list.update(handle_folder(directory / "prepend", auto))
        file_list.update(find_files_in_directory(directory / "prepend"))

    # If there's a sprites folder, process files in there first
    if (directory / "sprites").exists():
        file_list.update(handle_folder(directory / "sprites", auto))
        file_list.update(find_files_in_directory(directory / "sprites"))

    # Grab the vehicles
    file_list.update(find_files_in_directory(directory))

    # Automatically look at subdirectories
    if auto:
        # Don't automatically walk subdirectories
        exclude_dirs = {"append", "prepend", "sprites"}
        subdirectories = [p for p in directory.iterdir() if p.is_dir() and p.name not in exclude_dirs]
        for subdir in subdirectories:        
            file_list.update(handle_folder(subdir, True))
        

    if (directory / "append").exists():
        file_list.update(handle_folder(directory / "append", auto))
        file_list.update(find_files_in_directory(directory / "append"))

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

    src_directory = Path(src_directory_name)
    lang_directory = Path(lang_directory_name)
    gfx_directory = Path(gfx_directory_name)

    trains_directory = Path(src_directory_name) / Path("trains")
    trams_directory = Path(src_directory_name) / Path("trams")

    # Variant Headers
    variantheader_directory = Path()

    train_directories = {
        "multimode_mu",
        "electric_mu",
        "diesel_mu",
        "altfuel_mu",
        "multimode_loco",
        "electric_loco",
        "diesel_loco",
        "altfuel_loco",
        "steam_loco",
        "rolling_stock",
        "freight_wagon",
        "metro",
        "departmental",
        "utility_and_debug",
        "deprecated"
    }

    # Metro
    metro_directory = Path(trains_directory / "metro")


    nml_file = ""
    has_lang_dir = False

    # Add the special files to the internal nml file
    nml_file = append_file(src_directory / "grf.pnml", nml_file)

    file_list = dict()

    file_list.update(handle_folder(src_directory / "grf_prepend"))

    file_list.update(handle_folder(trains_directory))


    for directory in train_directories:
        filepath = trains_directory / directory / "sprites"
        file_list.update(handle_folder(filepath, False))

    file_list.update(handle_folder(trains_directory / "variantheader", True))

    file_list.update(handle_folder(trains_directory / "push_pull"))

    for directory in train_directories:
        filepath = trains_directory / directory
        file_list.update(handle_folder(filepath, True))    
    

    file_list.update(handle_folder(trams_directory, True))
    

    file_list.update(handle_folder(src_directory / "grf_append"))
    
    
    print("Finished finding pnml files\n")

    # Grab the raw list of files from the dictionary
    pnml_files = list()
    for files in file_list.values():
        pnml_files.extend(files)

    # Read the files into the buffer
    for file in pnml_files:
        # print("Reading '%s'" % ( file.stem + file.suffix))
        print(file)
        nml_file = append_file(file, nml_file)

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
