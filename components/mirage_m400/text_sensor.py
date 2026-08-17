import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor
from esphome.const import CONF_ID, CONF_NAME

from . import mirage_m400_ns, MirageM400Component, CONF_MIRAGE_M400_ID

# Define the C++ class for the sensor
MirageM400TextSensor = mirage_m400_ns.class_(
    "MirageM400TextSensor", text_sensor.TextSensor, cg.Component
)

# The ONLY schema allowed for a platform component
CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(MirageM400TextSensor),
    cv.Required(CONF_NAME): cv.string,
    cv.Required(CONF_MIRAGE_M400_ID): cv.use_id(MirageM400Component),
    cv.Optional("icon"): cv.string,
    cv.Optional("disabled_by_default", default=False): cv.boolean,
})

async def to_code(config, parent=None):
    # Create the C++ object
    var = cg.new_variable(config[CONF_ID], MirageM400TextSensor)
    await cg.register_component(var, config)

    # Ensure we have the parent hub (MirageM400Component)
    if parent is None:
        parent = await cg.get_variable(config[CONF_MIRAGE_M400_ID])

    # Link the sensor to the hub and the hub to the sensor
    cg.add(parent.register_text_sensor(var))
    cg.add(var.set_parent(parent))

    # Register it as a standard ESPHome text sensor
    await text_sensor.register_text_sensor(var, config)
