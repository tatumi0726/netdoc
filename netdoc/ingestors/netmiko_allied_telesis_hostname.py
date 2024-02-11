"""Ingestor for netmiko_allied_telesis_awplus_hostname."""
__remodeler__ = "tatumi0726"
__contact__ = "tatumi0726@gmail.com"
__copyright__ = "Copyright 2023, tatumi0726"
__license__ = "GPLv3"


from netdoc.schemas import device, discoverable
from netdoc import utils


def ingest(log):
    """Processing parsed output."""
    # See https://github.com/netbox-community/devicetype-library/tree/master/device-types
    vendor = "Allied Telesis"
    output = log.parsed_output

    # Parsing hostname
    try:
        name = output[len("hostname "):]
    except AttributeError as exc:
        raise AttributeError(f"Failed to match HOSTNAME regex on {name}") from exc
    name = utils.normalize_hostname(name)

    # Get or create Device
    data = {
        "name": name,
        "site_id": log.discoverable.site.id,
        "manufacturer": vendor,
    }
    device_o = device.get(name=data.get("name"))
    if not device_o:
        device_o = device.create(**data)

    if not log.discoverable.device:
        # Link Device to Discoverable
        discoverable.update(log.discoverable, device_id=device_o.id)

    # Update the log
    log.ingested = True
    log.save()
