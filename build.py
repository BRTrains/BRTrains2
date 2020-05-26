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
    if not filepath.exists():
        print("The file <%s> does not exist" % str(filepath))
        return -1

    with open(str(filepath)) as file:
        nml_file += "// " + filepath.stem + filepath.suffix + "\n"
        for line in file:
            nml_file += line
    nml_file += "\n\n"
    return nml_file


def find_pnml_files(src_directory: Path):
    file_list = []
    for path in src_directory.rglob("*.pnml"):
        if path.stem in ["railtypes", "grf", "templates"]:
            continue
        file_list.append(path)

    print("Found the following files: %s" %
          [str(file.stem + file.suffix) for file in file_list])
    return file_list


def write_file(filename: str, nml_file: str):
    filepath = Path(filename + ".nml")
    if filepath.exists():
        print("%s already exists.  Overwriting" % filename)

    with open(filepath, "w") as file_writer:
        for line in nml_file:
            file_writer.write(line)

    return 0


def compile_grf(has_lang_dir, grf_name, lang_dir):
    found_nml = util.find_spec("nml")
    if found_nml is not None:
        import nml.main
        parameters = []
        if has_lang_dir:
            parameters = ["--lang", str(lang_dir), grf_name + ".nml"]
        else:
            parameters = [grf_name + ".nml"]
        try:
            nml.main.main(parameters)
        except SystemExit:
            print("nml tried to exit but was stopped")
        print("Finished compiling grf file")
        return 1
    else:
        print("nml is not installed.  You can get it using 'pip install nml'")
        return -2


def main(grf_name, src_dir, lang_dir, gfx_dir, b_compile_grf, b_run_game):
    src_directory = Path("src")
    lang_directory = Path("lang")
    gfx_directory = Path("gfx")

    nml_file = ""
    has_lang_dir = False

    (has_lang_dir,
     error_code) = check_project_structure(src_directory, gfx_directory,
                                           lang_directory)
    if error_code != 0:
        return -1

    nml_file = copy_file(src_directory.joinpath("grf.pnml"), nml_file)
    nml_file = copy_file(src_directory.joinpath("railtypes.pnml"), nml_file)
    nml_file = copy_file(src_directory.joinpath("templates.pnml"), nml_file)

    file_list = find_pnml_files(src_directory)
    for file in reversed(file_list):
        print("Reading '%s'" % (file.stem + file.suffix))
        nml_file = copy_file(file, nml_file)

    if write_file(argv[-1], nml_file) != 0:
        print("The nml file failed to compile")
        return -1

    if b_compile_grf:
        return compile_grf(has_lang_dir, grf_name, lang_dir)

    return 0


if __name__ == "__main__":
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
    args = parser.parse_args()

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
        print("The nml file was compiled successfully")
