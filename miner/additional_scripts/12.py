import os


def __get_file_count_for_directories(path: str):
    top_level_directories = []
    top_level_files = []

    relevant_file_endings = [".ts", ".js", ".cs", ".css", ".scss", ".sass", ".html", ".bat", ".sh", ".cmd", ".ps1"]

    loc_counts = {}
    file_counts = {}

    for _, directories, files in os.walk(path):
        top_level_directories = directories
        top_level_files = files

        break

    ignored_files = 0

    for dir in top_level_directories:

        file_count = 0
        loc_count = 0

        for current_path, directories, files in os.walk(path + "/" + dir):
            if dir != ".vs" and dir != ".git" and not dir.endswith(".Migrations"):

                for filename in files:
                    matching = False
                    for ending in relevant_file_endings:
                        if filename.endswith(ending):
                            matching = True

                    if matching:

                        file_count += 1

                        try:
                            with open(current_path + "/" + filename, encoding="utf_8") as file:
                                loc_count += sum(1 for _ in file)
                        except:
                            ignored_files += 1


        loc_counts[dir] = loc_count
        file_counts[dir] = file_count

    total_loc = 0
    total_files = 0

    for dir in loc_counts:
        total_loc += loc_counts[dir]

    for dir in file_counts:
        total_files += file_counts[dir]

    loc_counts["total"] = total_loc
    file_counts["total"] = total_files

    print(loc_counts)
    print(file_counts)
    print(ignored_files)


if __name__ == "__main__":

    __get_file_count_for_directories("folder")

