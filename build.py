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
    if not src_directory.joinpath("templates.pnml").exists():
        print(
            "\"templates.pnml\" not found.  Assuming no templates are required"
        )

    print("Project structure is correct")
    return (has_lang_dir, 0)


def copy_file(filepath: Path, nml_file: str):
    # If the pnml filepath doesn't exist, exit
    if not filepath.exists():
        print("The file <%s> does not exist" % str(filepath))
        return -1

    # Read the pnml file into the internal nml
    with open(str(filepath), "w") as file:
        nml_file += "// " + filepath.stem + filepath.suffix + "\n"
        for line in file:
            nml_file += line
    nml_file += "\n\n"
    return nml_file


def find_pnml_files(src_directory: Path):
    file_list = []
    # Iterate through all files in src_directory recursively, finding any that end in .pnml
    for path in src_directory.rglob("*.pnml"):
        # Don't add the special ones
        if path.stem in ["railtypes", "grf", "templates"]:
            continue
        file_list.append(path)

    # List found files
    print("Found the following files: %s" %
          [str(file.stem + file.suffix) for file in file_list])
    return file_list


def write_file(filename: str, nml_file: str):
    # Generate the filepath and check if it exists
    filepath = Path(filename + ".nml")
    if filepath.exists():
        print("%s already exists.  Overwriting" % filename)

    # Write the internal nml to the file
    with open(filepath, "w") as file_writer:
        for line in nml_file:
            file_writer.write(line)

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
            parameters = ["--lang", str(lang_dir), grf_name + ".nml"]
        else:
            # If not, just the nml name
            parameters = [grf_name + ".nml"]
        try:
            # Try to compile the nml file
            nml.main.main(parameters)
        except SystemExit:
            # nml uses sys.exit(), so catch this to stop the program exiting
            print("nml tried to exit but was stopped")
        print("Finished compiling grf file")
        return 1
    else:
        # nml isn't installed
        print("nml is not installed.  You can get it using 'pip install nml'")
        return -2


def run_game(grf_name):
    from subprocess import run
    from sys import platform

    # Change default paths depending on whether we use Linux or Windows (sorry OSX)
    if platform.startswith("linux"):
        newgrf_dir = Path.home().joinpath(".openttd", "newgrf")
        executable_path = "/usr/bin/openttd"
    elif platform.startswith("win32"):
        newgrf_dir = Path.home().joinpath("Documents", "OpenTTD", "newgrf")
        executable_path = "C:/Program Files/OpenTTD/openttd.exe"

    json_read_ok = False
    # Check that the config file exists
    if Path("build.json").exists():
        from json import load, decoder
        with open("build.json") as json_data:
            # Try to read the config file
            try:
                data = load(json_data)
            # Errors if the file in invalid
            except decoder.JSONDecodeError:
                print("The config file is invalid")
                json_read_ok = False
            else:
                # Read successfully
                # Try to read the keys from the json file
                try:
                    newgrf_dir = data["newgrf_dir"]
                    executable_path = data["executable"]
                # Errors if not all keys are found
                except KeyError:
                    print("The config json file is invalid")
                    json_read_ok = False
                # Read successfully, set read_ok to true
                else:
                    json_read_ok = True

    # If reading the json didn't work
    if not json_read_ok:
        from json import dump
        from os import access, X_OK

        # Prompt the user for the "newgrf" directory until we get something like it
        while not Path(newgrf_dir).exists():
            newgrf_dir = input("Enter the newgrf directory: ")
            if len(newgrf_dir) > 6:
                newgrf_dir = "~/.openttd/newgrf"
                continue
            if newgrf_dir[-6:] != "newgrf":
                newgrf_dir = "~/.openttd/newgrf"

        # Prompt the user for the executable path until we get an executable
        while not Path(executable_path).exists():
            executable_path = input("Enter the OpenTTD executable path: ")
            if not (access(executable_path, X_OK)):
                executable_path = "/usr/bin/openttd"

        # Dump the two paths to a json file for next time
        with open("build.json", "w") as json_data:
            data = {
                "newgrf_dir": str(newgrf_dir),
                "executable": str(executable_path)
            }
            dump(data, json_data)

    # Copy the file to the newgrf directory
    from shutil import copy
    copy(grf_name + ".grf", Path(newgrf_dir))
    # Run the game in it's root directory
    run(executable=executable_path, args="", cwd=Path(executable_path).parent)
    return 2


def main(grf_name, src_dir, lang_dir, gfx_dir, b_compile_grf, b_run_game):
    src_directory = Path("src")
    lang_directory = Path("lang")
    gfx_directory = Path("gfx")

    nml_file = ""
    has_lang_dir = False

    # Check if the project is set up properly and we have a lang directory
    (has_lang_dir,
     error_code) = check_project_structure(src_directory, gfx_directory,
                                           lang_directory)
    if error_code != 0:
        return -1

    # Add the special files to the internal nml file
    nml_file = copy_file(src_directory.joinpath("grf.pnml"), nml_file)
    nml_file = copy_file(src_directory.joinpath("railtypes.pnml"), nml_file)
    nml_file = copy_file(src_directory.joinpath("templates.pnml"), nml_file)

    # Get a list of all the pnml files in src
    file_list = find_pnml_files(src_directory)
    # Read all the files into the internal nml
    for file in reversed(file_list):
        print("Reading '%s'" % (file.stem + file.suffix))
        nml_file = copy_file(file, nml_file)

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
        help="Run the game after compilation (will also compile the file)")
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
            "The grf file was compiled successfully and the game was started")
    else:
        print("The nml file was compiled successfully")
