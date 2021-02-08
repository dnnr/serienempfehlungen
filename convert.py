#!/usr/bin/env python3

import sys
import re

from pathlib import Path

from jinja2 import Template

TEMPLATE_FILE = "template.html"
LIMITATION_RE = re.compile(r"\(((?:[<=>]+ ~?)?S\d+)\)$")


def main():
    print(f"Reading list from {sys.argv[1]}", file=sys.stderr)
    listfile = Path(sys.argv[1])
    print(f"Writing to {sys.argv[2]}", file=sys.stderr)
    outfile = Path(sys.argv[2])

    raw_recommendations = listfile.read_text().splitlines()[2:]
    recommendations = []
    for raw_recommendation in raw_recommendations:
        recommendation = {
            "title": None,
            "must_see": False,
            "limitation": None,
        }
        if raw_recommendation.endswith(" *"):
            recommendation["must_see"] = True
            raw_recommendation = raw_recommendation[:-2]

        match = LIMITATION_RE.search(raw_recommendation)
        if match is not None:
            limitation = match.group(1)
            raw_recommendation = raw_recommendation[:-len(limitation)-2]
            recommendation["limitation"] = limitation

        recommendation["title"] = raw_recommendation.strip()

        recommendations.append(recommendation)

    template = Template(Path(TEMPLATE_FILE).read_text())
    output = template.render(recommendations=recommendations)
    print(output)

    outfile.write_text(output)


if __name__ == "__main__":
    main()
