import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import number
from esphome.const import CONF_ID, CONF_NAME
from . import mirage_m400_ns, MirageM400Component, CONF_MIRAGE_M400_ID

mirage_m400_ns = cg.esphome_ns.namespace("mirage_m400")
MirageM400Number = mirage_m400_ns.class_(
    "MirageM400Number", number.Number, cg.Component
)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(MirageM400Number),
        cv.Required("name"): cv.string,
        cv.Required(CONF_MIRAGE_M400_ID): cv.use_id(MirageM400Component),
        cv.Required("zone"): cv.int_range(min=1, max=16),
        cv.Optional("min_value", default=0): cv.float_,
        cv.Optional("max_value", default=100): cv.float_,
        cv.Optional("step", default=1): cv.float_,
        cv.Optional("icon"): cv.string,
    }
)

async def to_code(config, parent):
    var = cg.new_variable(config[CONF_ID], MirageM400Number)
    await cg.register_component(var, config)
    await number.register_number(var, config)
    cg.add(parent.register_number(var))
