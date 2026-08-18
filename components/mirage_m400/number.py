import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import number
from . import mirage_m400_ns, MirageM400Component
from .constants import *

DEPENDENCIES = ["mirage_m400"]

MirageM400Number = mirage_m400_ns.class_("MirageM400Number", number.Number)

CONFIG_SCHEMA = number.NUMBER_SCHEMA.extend({
    cv.Required(CONF_MIRAGE_M400_ID): cv.use_id(MirageM400Component),
    cv.Required(CONF_ZONE): cv.int_range(1, 17),
    cv.Optional("min_value", default=0): cv.float_range(0, 100),
    cv.Optional("max_value", default=100): cv.float_range(0, 100),
    cv.Optional("step", default=1): cv.float_,
})


async def to_code(config):
    hub = await cg.get_variable(config[CONF_MIRAGE_M400_ID])
    var = cg.new_Pvariable(
        config[CONF_ID],
        cg.RawExpression(f"(uint8_t){config[CONF_ZONE]}"),
    )
    await number.register_number(var, config)
    cg.add(hub.register_number(var))