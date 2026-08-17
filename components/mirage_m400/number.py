import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import number
from esphome.const import CONF_ID, CONF_NAME
from . import mirage_m400_ns, MirageM400Component, CONF_MIRAGE_M400_ID

mirage_m400_ns = cg.esphome_ns.namespace("mirage_m400")
MirageM400Number = mirage_m400_ns.class_(
    "MirageM400Number", number.Number, cg.Component
)

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(MirageM400Number),
    cv.Required("name"): cv.string,
    cv.Required(CONF_MIRAGE_M400_ID): cv.use_id(MirageM400Component),
    cv.Required("zone"): cv.int_range(min=1, max=16),
    cv.Optional("min_value", default=0): cv.float_,
    cv.Optional("max_value", default=100): cv.float_,
    cv.Optional("step", default=1): cv.float_,
    cv.Optional("icon"): cv.string,
    cv.Optional("disabled_by_default", default=False): cv.boolean,
    cv.Optional("restore_mode", default="RESTORE_DEFAULT_OFF"): cv.string,
})

async def to_code(config):
    # Create the C++ object
    var = cg.new_variable(config[CONF_ID], MirageM400Number)
    await cg.register_component(var, config)

    # Look up the parent hub
    parent = await cg.get_variable(config[CONF_MIRAGE_M400_ID])

    # Link the number to the hub
    cg.add(parent.register_number(var))
    cg.add(var.set_parent(parent))

    # Register with the ESPHome core, explicitly passing the required values
    await number.register_number(
        var,
        config,
        min_value=config["min_value"],
        max_value=config["max_value"],
        step=config["step"]
    )
