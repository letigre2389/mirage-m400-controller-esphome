import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import number
from esphome.const import CONF_ID, CONF_NAME

from . import mirage_m400_ns, MirageM400Component

DEPENDENCIES = ["mirage_m400"]

CONF_ZONE = "zone"

MirageNumber = mirage_m400_ns.class_("MirageNumber", number.Number, cg.Component)

CONFIG_SCHEMA = number.NUMBER_SCHEMA.extend(
    {
        cv.GenerateID(): cv.declare_id(MirageNumber),
        cv.GenerateID("mirage_m400_id"): cv.use_id(MirageM400Component),
        cv.Required(CONF_ZONE): cv.int_range(min=1, max=16),
    }
)


async def to_code(config):
    parent = await cg.get_variable(config["mirage_m400_id"])
    var = cg.new_Pvariable(config[CONF_ID], parent, config[CONF_ZONE])
    
    await number.register_number(var, config)
    await cg.register_component(var, config)
