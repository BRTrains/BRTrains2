from pathlib import Path
from sys import argv
from os import system


def check_project_structure(src_directory : Path, gfx_directory : Path, lang_directory : Path):
    # Check that the project is properly structured
    if not src_directory.exists():
        print("\"src\" directory not found.  Aborting")
        return -1
    if not gfx_directory.exists():
        print("\"gfx\" directory not found.  Aborting")
        return -1
    if not lang_directory.exists():
        print("\"lang\" directory not found.  Assuming hard-coded strings (this is not best practice)")
    

    # Find the grf, railtypes, and templates files
    if not src_directory.joinpath("grf.pnml").exists():
        print("\"grf.pnml\" not found.  It should be in \"src\" and contain the grf block")
        return -1
    if not src_directory.joinpath("railtypes.pnml").exists():
        print("\"railtypes.pnml\" not found.  It should be in \"src\" and contain the railtypetable block")
        return -1
    if not src_directory.joinpath("templates.pnml").exists():
        print("\"templates.pnml\" not found.  Assuming no templates are required")

    print("Project structure is correct")
    return 0


def copy_file(filepath : Path, nml_file : str):
    if not filepath.exists():
        print("The file <%s> does not exist" % str(filepath))
        return -1

    with open(str(filepath)) as file:
        nml_file += "// " + filepath.stem + filepath.suffix + "\n"
        for line in file:
            nml_file += line
    nml_file += "\n\n"
    return nml_file


def find_pnml_files(src_directory : Path):
    file_list = []
    for path in src_directory.rglob("*.pnml"):
        if path.stem in ["railtypes", "grf", "templates"]:
            continue
        file_list.append(path)
    
    print("Found the following files: %s" % [str(file.stem + file.suffix) for file in file_list])
    return file_list


def write_file(filename : str, nml_file : str):
    filepath = Path(filename)
    if filepath.exists():
        print("%s already exists.  Overwriting" % filename)


    with open(filepath, "w") as file_writer:
        for line in nml_file:
            file_writer.write(line)

    return 0


def main():
    src_directory = Path("./src")
    lang_directory = Path("./lang")
    gfx_directory = Path("./gfx")

    nml_file = ""

    if check_project_structure(src_directory, gfx_directory, lang_directory) != 0:
        return -1

    nml_file = copy_file(src_directory.joinpath("grf.pnml"), nml_file)
    nml_file = copy_file(src_directory.joinpath("railtypes.pnml"), nml_file)
    nml_file = copy_file(src_directory.joinpath("templates.pnml"), nml_file)

    file_list = find_pnml_files(src_directory)
    for file in reversed(file_list):
        print("Reading '%s'" % (file.stem + file.suffix))
        nml_file = copy_file(file, nml_file)

    if write_file(argv[1], nml_file) != 0:
        print("The nml file failed to compile")
        return -1

    # Evil but it works
    compile_command = "nmlc -l lang " + argv[1]
    system(compile_command)
    return 0


if __name__ == "__main__":
    error_code = main()
    if (error_code != 0):
        print("The program failed to execute properly.  Please consult the log")
    else:
        print("grf file compiled successfully")