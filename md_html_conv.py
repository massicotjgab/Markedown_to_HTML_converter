import argparse
import os
from pathlib import Path
import re

parser = argparse.ArgumentParser(
    description="convert a markedown directory in a new html directory"
)
parser.add_argument(
    "-i", "--imput-directory", help="directory you want to convert"
)
parser.add_argument(
    "-o", "--output-directory", help="where your directory will be converted"
)
args = parser.parse_args()

to_convert = os.path.abspath(args.imput_directory)
where_convert = os.path.abspath(args.output_directory)
way_conv = Path(to_convert)
list_file_to_conv = way_conv.glob("**/*.markdown")

im_an_url = r"(http(s)?://[a-z0-9]+\.[a-z0-9]+)"
be_a_list = False

for file_to_conv in list_file_to_conv:
    new_text = ""
    os.chdir(to_convert)
    with open(file_to_conv, "r", encoding="utf-8") as file_in_conv:
        for line in file_in_conv:
            new_line = line

            # important text function
            def em_func():
                incmt = 0
                while "*" in new_line:
                    i = new_line.count("*")
                    halfi = i / 2
                    while incmt <= halfi:
                        index_star = new_line.index("*")
                        new_line = (
                            new_line[:index_star] + "<em>" + new_line[index_star + 1 :]
                        )
                        incmt += 1
                    while incmt <= i:
                        index_star = new_line.index("*")
                        new_line = (
                            new_line[:index_star] + "</em>" + new_line[index_star + 1 :]
                        )
                        incmt += 1
                    return new_line

            # TITLE conversion
            if "#" in new_line:
                while new_line[-1] == "#":
                    new_line = new_line[:-1]
                nb_h = new_line.count("#")
                title_tag = f"<h{nb_h}"
                new_line = (
                    title_tag
                    + new_line[nb_h:-1]
                    + (title_tag[:1] + "/" + title_tag[1:])
                    + "\n"
                )

            # STAR conversion : LIST conversion, including important text
            if "*" in new_line:
                new_line = new_line.strip()
                nb_star = new_line.count("*")
                if nb_star % 2 != 0:
                    if new_line[0] == "*":
                        ftag = "<li>"
                        ltag = "</li>\n"
                        list_ftag = "<ul>\n"
                        list_ltag = "</ul>\n"
                        if not be_a_list:
                            new_text += list_ftag
                            be_a_list = True
                        new_line = ftag + line[1:] + ltag
                    elif be_a_list:
                        new_text += list_ltag
                        be_a_list = False
                    em_func()  # important text function
                elif nb_star % 2 == 0:
                    em_func()  # important text function

            # URL conversion
            if re.search(im_an_url, new_line) is not None:
                new_line = re.sub(im_an_url, '<a href="\\1">\\1</a>', new_line)

            new_text += new_line
        os.chdir(where_convert)
        converted_file = str(file_to_conv)[
            str(file_to_conv).rindex("/") + 1 : str(file_to_conv).index(".")
        ]
        with open(f"{converted_file}.html", "w", encoding="utf-8") as final_file:
            final_file.write(new_text)
            print("Done! Thanks for using this script")
###
