import os
import requests

urls = [
    "https://cdn.jsdelivr.net/gh/Elysian-Realme/FuGfConfig@main/ConfigFile/Surge/Apple/AppleCDNRules.conf",
    "https://cdn.jsdelivr.net/gh/Elysian-Realme/FuGfConfig@main/ConfigFile/Surge/Apple/AppleUpdateRules.conf"
]

combined_content = ""

for url in urls:
    response = requests.get(url)
    combined_content += response.text + "\n"

domains = set()
domain_suffixes = set()

# Parse lines
def parse_line(line):
    if line.startswith("#") or line == "":
        return f"  {line}"
    elif line.startswith("DOMAIN,"):
        domain = line.split(",")[1]
        if domain not in domains:
            domains.add(domain)
            return f"  - '{domain}'"
        return f""
    elif line.startswith("DOMAIN-SUFFIX,"):
        domain_suffix = line.split(",")[1]
        if domain_suffix not in domain_suffixes:
            domain_suffixes.add(domain_suffix)
            return f"  - '+.{domain_suffix}'"
        return f""
    else:  # unknown types
        return f"  # {line}"
    
# Create a new file in the same directory as this script
file_path = os.path.join(os.path.dirname(__file__), "AppleCDN.yaml")
with open(file_path, "w") as file:
    file.write("# Ref: https://cdn.jsdelivr.net/gh/Elysian-Realme/FuGfConfig@main/ConfigFile/Surge/Apple/AppleCDNRules.conf\n")
    file.write("# Ref: https://cdn.jsdelivr.net/gh/Elysian-Realme/FuGfConfig@main/ConfigFile/Surge/Apple/AppleUpdateRules.conf\n")
    file.write("payload:\n")
    for line in combined_content.splitlines():
        parsed_line = parse_line(line)
        if parsed_line != "":
            file.write(parsed_line + "\n")