# SPDX-FileCopyrightText: 2022 Diego Elio Pettenò
#
# SPDX-License-Identifier: 0BSD

import pathlib

import click
import cmarkgfm
import jinja2
from pygal.maps import world

UNIT_TO_COUNTRIES = {
    "mg/dL": {
        "it": "https://www.salute.gov.it/portale/nutrizione/dettaglioContenutiNutrizione.jsp?lingua=italiano&id=5511&area=nutrizione&menu=croniche&tab=4",
        "us": None,
    },
    "mmol/L": {
        "gb": "https://www.nhs.uk/conditions/high-blood-sugar-hyperglycaemia/",
        "ie": "https://www2.hse.ie/conditions/type-2-diabetes/treatment/medicine/",
        "cn": None,
    },
}


def render_worldmap(output_file: pathlib.Path) -> None:
    worldmap = world.World()

    for unit, countries in UNIT_TO_COUNTRIES.items():
        worldmap.add(unit, countries.keys())

    worldmap.render_to_file(output_file)


def render_pages(output_directory: pathlib.Path) -> None:
    jinja_env = jinja2.Environment(
        loader=jinja2.PackageLoader("world_glucometer_units")
    )
    template = jinja_env.get_template("index.md")

    countries_to_unit = {}
    for unit, countries in UNIT_TO_COUNTRIES.items():
        for (country, reference) in countries.items():
            countries_to_unit[country] = (unit, reference)

    rendered_markdown = template.render(countries_to_unit=countries_to_unit)
    (output_directory / "index.html").write_text(
        cmarkgfm.github_flavored_markdown_to_html(rendered_markdown)
    )


@click.command()
@click.option(
    "--output-directory",
    type=click.Path(dir_okay=True, file_okay=False, exists=True, writable=True),
    default=".",
)
def main(output_directory: str) -> None:
    output_directory = pathlib.Path(output_directory)
    render_worldmap(output_directory / "worldmap.svg")
    render_pages(output_directory)


if __name__ == "__main__":
    main()
