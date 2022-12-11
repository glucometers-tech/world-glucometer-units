# SPDX-FileCopyrightText: 2022 Diego Elio Pettenò
#
# SPDX-License-Identifier: 0BSD

import pathlib

import click
from pygal.maps import world

UNIT_TO_COUNTRIES = {
    "mg/dL": {
        "it",  # https://www.salute.gov.it/portale/nutrizione/dettaglioContenutiNutrizione.jsp?lingua=italiano&id=5511&area=nutrizione&menu=croniche&tab=4
        "us",
    },
    "mmol/L": {
        "gb",  # https://www.nhs.uk/conditions/high-blood-sugar-hyperglycaemia/
        "ie",  # https://www2.hse.ie/conditions/type-2-diabetes/treatment/medicine/
        "cn",
    },
}


@click.command()
@click.option(
    "--output-directory",
    type=click.Path(dir_okay=True, file_okay=False, exists=True, writable=True),
    default=".",
)
def main(output_directory: str) -> None:
    worldmap = world.World()
    for unit, countries in UNIT_TO_COUNTRIES.items():
        worldmap.add(unit, countries)

    worldmap.render_to_file(pathlib.Path(output_directory) / "worldmap.svg")


if __name__ == "__main__":
    main()
