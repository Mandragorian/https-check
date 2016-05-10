"""This file is part of https-check.

https-check is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

https-check is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with https-check.  If not, see <http://www.gnu.org/licenses/>.

Copyright (C)  Konstantinos Andrikpoulos <gkonstandinos@gmail.com>
"""

import yaml
import requests
import argparse
import sys

def create_ruleset(base_dir, https_enabled_subdirs, outfile):
    preamble = "<ruleset name='%s'>\n" % base_dir
    epilogue = ("\n\n   <rule from='^http:'\n"
                "         to='https:' />\n"
                "</ruleset>\n"
                    )
    targets = [ "   <target host='%s' />" % url for url in https_enabled_subdirs]
    body = "\n".join(targets)
    outfile.write(preamble + body + epilogue)


if __name__ == "__main__":


    parser = argparse.ArgumentParser(description="Probe domain name for https support.")
    ruleset_group = parser.add_argument_group('ruleset generation')

    parser.add_argument('--infile',
            type=argparse.FileType('r'),
            default=sys.stdin,
            help='a file containing some base directories and their subdirs in yaml format')

    ruleset_group.add_argument('--create-ruleset',
            action='store_true',
            default=False,
            help= 'specify if a HttpsEverywhere ruleset should be created')

    ruleset_group.add_argument('--ruleset-file',
            type=argparse.FileType('w'),
            default=sys.stdout,
            help='outputs HttpsEverywhere ruleset for this site in specified file')

    args = parser.parse_args()


    subdomains_list_file =args.infile
    should_create_ruleset = args.create_ruleset
    ruleset_output_file = args.ruleset_file
    checking_time = (2,5)

    https_enabled_subdirs = []
    try:
        sites = yaml.load(subdomains_list_file)
    except yaml.YAMLError as exc:
        print(exc)

    for site in sites:
        base_dir = site["base_dir"]
        subdirs = site["subdomains"]
        urls = [ "".join([subdir, ".", base_dir])
                for subdir in subdirs]
        for url in urls:
            try:
                r = requests.get("https://" + url, timeout=checking_time)
            except requests.exceptions.ConnectTimeout as exc:
                print("this url:", url, "has no https enabled")
            except requests.exceptions.ConnectionError as exc:
                print("unable to decide https for url:", url)
            else:
                https_enabled_subdirs.append(url)
                print("this url:", url, "has https enabled")

    if should_create_ruleset:
        create_ruleset("ntua.gr", https_enabled_subdirs, ruleset_output_file)
