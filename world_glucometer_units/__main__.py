# SPDX-FileCopyrightText: 2022 Diego Elio Pettenò
#
# SPDX-License-Identifier: 0BSD

import pathlib
import textwrap

import click
import cmarkgfm
import pycountry
import jinja2
from pygal.maps import world

UNIT_TO_COUNTRIES = {
    "mg/dL": {
        "de": None,
        "it": "https://www.salute.gov.it/portale/nutrizione/dettaglioContenutiNutrizione.jsp?lingua=italiano&id=5511&area=nutrizione&menu=croniche&tab=4",
        "us": None,
    },
    "mmol/L": {
        "cn": None,
        "gb": "https://www.nhs.uk/conditions/high-blood-sugar-hyperglycaemia/",
        "ie": "https://www2.hse.ie/conditions/type-2-diabetes/treatment/medicine/",
        "no": "https://www.diabetes.no/diabetes-type-1/behandling/blodsukker/",
    },
    "both": {
        "pl": None,
    },
}


def render_worldmap(output_file: pathlib.Path) -> None:
    worldmap = world.World()

    for unit, countries in UNIT_TO_COUNTRIES.items():
        worldmap.add(unit, countries.keys())

    worldmap.render_to_file(output_file)


HTML_PREAMBLE = textwrap.dedent(
    """\
    <link rel="icon" href="/favicon.ico" sizes="any"><!-- 32×32 -->
    <link rel="icon" href="/favicon.svg" type="image/svg+xml">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png"><!-- 180×180 -->
    """
)


def render_markdown(output_path: pathlib.Path, content: str) -> None:
    output_path.write_text(HTML_PREAMBLE + content, encoding="utf-8")


def render_pages(output_directory: pathlib.Path) -> None:
    jinja_env = jinja2.Environment(
        loader=jinja2.PackageLoader("world_glucometer_units")
    )
    template = jinja_env.get_template("index.md")

    countries_to_unit = {}
    for unit, countries in UNIT_TO_COUNTRIES.items():
        for (country_code, reference) in countries.items():
            country = pycountry.countries.lookup(country_code)
            countries_to_unit[country.name] = (unit, reference)

    rendered_markdown = template.render(countries_to_unit=countries_to_unit)
    render_markdown(
        output_directory / "index.html",
        cmarkgfm.github_flavored_markdown_to_html(
            rendered_markdown, options=cmarkgfm.cmark.Options.CMARK_OPT_UNSAFE
        ),
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
