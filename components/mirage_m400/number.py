import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import number
from esphome.const import CONF_ID

from . import CONF_MIRAGE_M400_ID, MirageM400Component, mirage_m400_ns

CONF_ZONE = "zone"

MirageVolumeNumber = mirage_m400_ns.class_(
    "MirageVolumeNumber", number.Number, cg.Component
)

CONFIG_SCHEMA = (
    number.number_schema(MirageVolumeNumber)
    .extend(
        {
            cv.GenerateID(CONF_MIRAGE_M400_ID): cv.use_id(MirageM400Component),
            cv.Required(CONF_ZONE): cv.int_range(min=1, max=32),
        }
    )
    .extend(cv.COMPONENT_SCHEMA)
)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_MIRAGE_M400_ID])
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    # Protocol volume range is 0x00-0xA0 (0-160 decimal), integer steps.
    await number.register_number(var, config, min_value=0, max_value=160, step=1)
    cg.add(var.set_parent(parent))
    cg.add(var.set_zone(config[CONF_ZONE]))
