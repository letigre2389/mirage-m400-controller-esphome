import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import number
from .constants import *

DEPENDENCIES = ["mirage_m400"]

mirage_m400_ns = cg.esphome_ns.namespace("mirage_m400")
MirageM400Number = mirage_m400_ns.class_(
    "MirageM400Number", number.Number, cg.Component
)

CONFIG_SCHEMA = number.number_schema(MirageM400Number).extend({
    cv.Required(CONF_MIRAGE_M400_ID): cv.use_id(mirage_m400_ns.class_("MirageM400Component")),
    cv.Required(CONF_ZONE): cv.int_range(min=1, max=17),
})


async def to_code(config):
    hub = await cg.get_variable(config[CONF_MIRAGE_M400_ID])
    var = cg.new_Pvariable(config[cv.CONF_ID], hub)
    
    await number.register_number(
        var,
        config,
        min_value=0,
        max_value=100,
        step=1
    )