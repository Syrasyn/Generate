"""Interactively generate a TLA units YAML inventory."""

from pathlib import Path

import yaml


UNIT_FIELDS = ("name", "type", "idf", "hrcount", "port")
OUTPUT_DIR = Path("output")


class InlineMapping(dict):
	"""Mapping type rendered on one YAML line."""


class QuotedString(str):
	pass


class UnitsDumper(yaml.SafeDumper):
	pass


def represent_inline_mapping(dumper, value):
	node = dumper.represent_dict(value)
	node.flow_style = True
	return node


UnitsDumper.add_representer(InlineMapping, represent_inline_mapping)
UnitsDumper.add_representer(
	QuotedString,
	lambda dumper, value: dumper.represent_scalar(
		"tag:yaml.org,2002:str", value, style="'"
	),
)


def prompt_count():
	while True:
		value = input("Enter the number of predetermined interfaces: ").strip()
		try:
			count = int(value)
		except ValueError:
			print("Please enter a whole number.")
			continue
		if count >= 0:
			return count
		print("Please enter zero or a positive number.")


def prompt_unit(number):
	print(f"Enter values for unit {number}:")
	return InlineMapping(
		{
			field: QuotedString(input(f"  {field}: ").strip())
			for field in UNIT_FIELDS
		}
	)


def collect_units():
	return {"units": [prompt_unit(number) for number in range(1, prompt_count() + 1)]}


def main():
	output_path = input("Output file [output/generated_units.yml]: ").strip() or "generated_units.yml"
	destination = Path(output_path)
	if destination.parent == Path("."):
		destination = OUTPUT_DIR / destination
	destination.parent.mkdir(parents=True, exist_ok=True)
	with destination.open("w", encoding="utf-8", newline="\n") as output_file:
		yaml.dump(
			collect_units(),
			output_file,
			Dumper=UnitsDumper,
			sort_keys=False,
			default_flow_style=False,
			width=4096,
		)
	print(f"Wrote {destination}")


if __name__ == "__main__":
	main()
