import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from esphome.const import CONF_ID, CONF_NAME
from . import mirage_m400_ns, MirageM400Component, CONF_MIRAGE_M400_ID

mirage_m400_ns = cg.esphome_ns.namespace("mirage_m400")
MirageM400Switch = mirage_m400_ns.class_(
    "MirageM400Switch", switch.Switch, cg.Component
)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(MirageM400Switch),
        cv.Required("name"): cv.string,
        cv.Required(CONF_MIRAGE_M400_ID): cv.use_id(MirageM400Component),
        cv.Required("zone"): cv.int_range(min=1, max=16),
        cv.Required("type"): cv.enum({"power": 0, "mute": 1}),
        cv.Optional("icon"): cv.string,
        cv.Optional("disabled_by_default", default=False): cv.boolean,
    }
)

async def to_code(config):
    var = cg.new_variable(config[CONF_ID], MirageM400Switch)
    await cg.register_component(var, config)

    parent = await cg.get_variable(config[CONF_MIRAGE_M400_ID])

    cg.add(parent.register_switch(var))
    cg.add(var.set_parent(parent))

    await switch.register_switch(var, config)
