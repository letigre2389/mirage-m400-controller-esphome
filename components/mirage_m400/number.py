import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import number
from esphome.const import CONF_ID, UNIT_PERCENT

CODEOWNER = ["@yourusername"]
DEPENDENCIES = ["mirage_m400"]

CONF_MIRAGE_M400_ID = "mirage_m400_id"
CONF_ZONE = "zone"

mirage_m400_ns = cg.esphome_ns.namespace("mirage_m400")
MirageM400Number = mirage_m400_ns.class_("MirageM400Number", number.Number)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(MirageM400Number),
        cv.GenerateID(CONF_MIRAGE_M400_ID): cv.use_id(cg.Component),
        cv.Required(CONF_ZONE): cv.int_range(min=1, max=16),
        cv.Optional("min_value", default=0): cv.float_,
        cv.Optional("max_value", default=100): cv.float_,
        cv.Optional("step", default=1): cv.float_,
    }
).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    var = cg.new_variable(config[CONF_ID], MirageM400Number)
    mirage = await cg.get_variable(config[CONF_MIRAGE_M400_ID])
    cg.add(var.set_parent(mirage))
    cg.add(mirage.register_number(var, config[CONF_ZONE]))
