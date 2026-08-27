"""Interactively generate the device and VLAN YAML inventory."""

from pathlib import Path

import yaml


DEVICE_SECTIONS = ("brocade", "cisco", "juniper", "nokia", "nokiaaltiplano")
DEVICE_FIELDS = (
	"hostname",
	"model",
	"uplinklag",
	"mgmtip",
	"customer",
	"idf",
	"submdf",
	"wifi",
	"secnet",
	"doors",
	"l3",
)
VLAN_FIELDS = ("description", "vlanid", "dhcp", "mgmt")
OUTPUT_DIR = Path("output")


class InlineMapping(dict):
	"""Mapping type rendered on one YAML line."""


class QuotedString(str):
	pass


class InventoryDumper(yaml.SafeDumper):
	pass


def represent_inline_mapping(dumper, value):
	node = dumper.represent_dict(value)
	node.flow_style = True
	return node


InventoryDumper.add_representer(InlineMapping, represent_inline_mapping)
InventoryDumper.add_representer(
	type(None),
	lambda dumper, value: dumper.represent_scalar("tag:yaml.org,2002:null", ""),
)
InventoryDumper.add_representer(
	QuotedString,
	lambda dumper, value: dumper.represent_scalar("tag:yaml.org,2002:str", value, style="'"),
)


def prompt_count(label):
	while True:
		value = input(f"Number of {label}: ").strip()
		try:
			count = int(value)
		except ValueError:
			print("Please enter a whole number.")
			continue
		if count >= 0:
			return count
		print("Please enter zero or a positive number.")


def prompt_entry(fields, label, number):
	print(f"Enter values for {label} {number}:")
	return {
		field: QuotedString(input(f"  {field}: ").strip())
		for field in fields
	}


def collect_inventory():
	inventory = {section: None for section in DEVICE_SECTIONS}

	for section in DEVICE_SECTIONS:
		count = prompt_count(f"{section} devices")
		if count:
			inventory[section] = [
				InlineMapping(prompt_entry(DEVICE_FIELDS, section, number))
				for number in range(1, count + 1)
			]

	vlan_count = prompt_count("VLANs")
	inventory["vlans"] = [
		InlineMapping(prompt_entry(VLAN_FIELDS, "VLAN", number))
		for number in range(1, vlan_count + 1)
	]
	return inventory


def main():
	output_path = input("Output file [output/generated.yml]: ").strip() or "generated.yml"
	inventory = collect_inventory()
	destination = Path(output_path)
	if destination.parent == Path("."):
		destination = OUTPUT_DIR / destination
	destination.parent.mkdir(parents=True, exist_ok=True)
	with destination.open("w", encoding="utf-8", newline="\n") as output_file:
		yaml.dump(
			inventory,
			output_file,
			Dumper=InventoryDumper,
			sort_keys=False,
			default_flow_style=False,
			width=4096,
		)
	print(f"Wrote {destination}")


if __name__ == "__main__":
	main()
