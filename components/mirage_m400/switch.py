import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from esphome.const import CONF_ID

mirage_m400_ns = cg.esphome_ns.namespace("mirage_m400")
MirageM400Switch = mirage_m400_ns.class_(
    "MirageM400Switch", switch.Switch, cg.Component
)

SWITCH_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(MirageM400Switch),
        cv.Required("name"): cv.string,
        cv.Required("zone"): cv.int_range(min=1, max=16),
        cv.Required("type"): cv.enum({"power": 0, "mute": 1}),
    }
)

async def to_code(config, parent):
    var = cg.new_variable(config[CONF_ID], MirageM400Switch)
    await cg.register_component(var, config)
    await switch.register_switch(var, config)
    cg.add(parent.register_switch(var))
