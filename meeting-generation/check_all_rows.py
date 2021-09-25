import csv
import os
import argparse
import re

def check_all_rows(ifile, ofile):
    # First, build a set of all input emails
    emails = set()
    with open(ifile, "r") as input:
        in_reader = csv.DictReader(input)

        for row in in_reader:
            email = row["email"]
            emails.add(email)
    
    # Second, build a dictionary of all output emails -> links pairs
    links_dict = {}
    with open(ofile, "r") as output:
        out_reader = csv.DictReader(output)

        for row in out_reader:
            email, link = row["email"], row["link"]
            links_dict[email] = link

    all_clear = True
    # Check that every input email had a corresponding
    for email in emails:
        if email not in links_dict:
            print(f"No output entry found! Email {email}")
            all_clear = False
            continue    

    
    # Check that every output entry also had a corresponding input entry, and a unique valid link
    zoom_link_re = re.compile(r"https:\/\/berkeley.zoom.us\/j\/([0-9]{11})\?pwd=([a-zA-Z0-9]){32}")
    links_set = set()
    for email, link in links_dict.items():
        if email not in emails:
            print(f"No input entry found! Email {email} Link {link}")
            all_clear = False
            continue

        if not zoom_link_re.match(link):
            print(f"Failed regex check for link validity! Email {email} Link {link}")
            all_clear = False
            continue

        if link in links_set:
            print(f"Link was already used previously! Email {email} Link {link}")
            all_clear = False
            continue

        links_set.add(link)

    if all_clear:
        print("Hooray! Everything passed :)")
    else:
        print("There was an error! See output above.")


if __name__ == "__main__":

    ap = argparse.ArgumentParser(description="Verify a bidirectional map between CSV of emails and CSV of email->Zoom link pairs")

    ap.add_argument("input_file", help="The input file with a .CSV of emails to verify")
    ap.add_argument("output_file", help="The output file with a .CSV of emails and links to check against input")

    args = ap.parse_args()
    ifile = args.input_file
    ofile = args.output_file

    check_all_rows(ifile, ofile)