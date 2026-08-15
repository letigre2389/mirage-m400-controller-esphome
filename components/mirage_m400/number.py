import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import number
from esphome.const import CONF_ID

from . import mirage_m400_ns, MirageM400Component, CONF_MIRAGE_M400_ID

DEPENDENCIES = ["mirage_m400"]

CONF_ZONE = "zone"

MirageM400Number = mirage_m400_ns.class_("MirageM400Number", number.Number)

CONFIG_SCHEMA = number.number_schema(MirageM400Number).extend(
    {
        cv.GenerateID(CONF_MIRAGE_M400_ID): cv.use_id(MirageM400Component),
        cv.Required(CONF_ZONE): cv.int_range(min=1, max=16),
    }
)

async def to_code(config):
    parent = await cg.get_variable(config[CONF_MIRAGE_M400_ID])
    var = await number.new_number(config)
    cg.add(parent.register_number(var))
    cg.add(var.set_zone(config[CONF_ZONE]))
