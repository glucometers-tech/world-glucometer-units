<!--
SPDX-FileCopyrightText: 2022 Diego Elio Pettenò

SPDX-License-Identifier: 0BSD
-->
# Blood Sugar Level Units Worldwide

Blood sugar level (also known as glycaemia) is the measure of glucose concentrated in
the blood.

There are two main unit of measures used for this attribute: mg/dL and mmol/L, which
have a fixed 18:1 ratio. Different countries use different units, and there isn't a
clear to know which country uses what, until now!

![World Map With Units](worldmap.svg)

## Table and References

| Country | Unit |
|---------|------|
{%- for (country, (unit, reference)) in countries_to_unit.items() %}
| {{country}} | {% if reference == None %}{{unit}}{% else %}[{{unit}}]({{reference}}){% endif %} |
{%- endfor %}

## Contributing

If you want to include a new country, please [check the GitHub repository](
https://github.com/glucometers-tech/world-glucometer-units)!

Currently both units and references are hardcoded in the Python source code, but
improvements are welcome.

If there is any way to migrate the references into [Wikidata](https://www.wikidata.org/)
and render this page from it, it would be very welcome, as it would provide a lot more
useful.
