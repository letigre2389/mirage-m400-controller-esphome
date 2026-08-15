import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import number
from esphome.const import (
    CONF_ID,
    UNIT_PERCENT,
    ICON_VOLUME_HIGH,
)

CODEOWNER = ["@yourusername"]
DEPENDENCIES = ["mirage_m400"]

CONF_MIRAGE_M400_ID = "mirage_m400_id"
CONF_ZONE = "zone"

mirage_m400_ns = cg.esphome_ns.namespace("mirage_m400")

CONFIG_SCHEMA = number.number_schema().extend(
    {
        cv.GenerateID(CONF_MIRAGE_M400_ID): cv.use_id(cg.Component),
        cv.Required(CONF_ZONE): cv.int_range(min=1, max=16),
    }
)

async def to_code(config):
    var = await number.new_number(
        config,
        min_value=0,
        max_value=100,
        step=1,
    )
    mirage = await cg.get_variable(config[CONF_MIRAGE_M400_ID])
    cg.add(var.set_parent(mirage))
    cg.add(mirage.register_number(var, config[CONF_ZONE]))
