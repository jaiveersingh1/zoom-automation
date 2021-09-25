import csv
import argparse

def generate_email_content(input_file, output_file, names_file = None):
    names_dict = None
    if names_file is not None:
        names_dict = {}
        with open(names_file, "r") as input_names:
            reader = csv.DictReader(input_names)

            for row in reader:
                name, email = row["name"], row["email"]

                delimiter_index = name.find(", ")
                fullname = f"{name[delimiter_index + 2:]} {name[:delimiter_index]}"

                names_dict[email] = fullname

    with open(input_file, "r") as input:
        reader = csv.DictReader(input)
    
        with open(output_file, "w+") as output:
            fieldnames = ['email', 'content']
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                email, link = row["email"], row["link"]

                name = names_dict[email] if names_dict is not None else "EECS 16B Student"

                # Note that this f-string has to be formatted in this weird indentation to avoid adding indentation to the actual email
                email_body = (
f"""Hi {name},

This email contains Important Exam Information for EECS 16B.

Please save this email or link somewhere you know you can find it later!

Your individual Zoom link for all EECS 16B exams is below:
{link} 

Thank you!
Your EECS 16B Course Staff
"""
)

                writer.writerow({'email': email, 'content': email_body})



if __name__ == "__main__":

    ap = argparse.ArgumentParser(description="Prepare exam Zoom link output for YAMM mass email sending")
    ap.add_argument(
        "input_file",
        help="Input .csv file from meeting generation script"
    )
    ap.add_argument(
        "--names",
        "-n",
        help="Additional .csv containing student names",
        default=None
    )
    ap.add_argument(
        "--output_file",
        "-o",
        help="Output .csv file for use with YAMM",
        default="yamm_output.csv"
    )
    args = ap.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    names_file = args.names

    generate_email_content(input_file, output_file, names_file)


