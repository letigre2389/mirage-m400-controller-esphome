import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor
from esphome.const import CONF_ID, CONF_NAME

mirage_m400_ns = cg.esphome_ns.namespace("mirage_m400")
MirageM400TextSensor = mirage_m400_ns.class_(
    "MirageM400TextSensor", text_sensor.TextSensor, cg.Component
)

TEXT_SENSOR_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(MirageM400TextSensor),
        cv.Required("name"): cv.string,
    }
)

async def to_code(config, parent):
    var = cg.new_variable(config[CONF_ID], MirageM400TextSensor)
    await cg.register_component(var, config)
    await text_sensor.register_text_sensor(var, config)
    cg.add(parent.register_text_sensor(var))
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor
from esphome.const import CONF_ID

from . import mirage_m400_ns, MirageM400Component, CONF_MIRAGE_M400_ID

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(MirageM400TextSensor),
    cv.Required(CONF_NAME): cv.string,
    cv.Required(CONF_MIRAGE_M400_ID): cv.use_id(MirageM400Component),
})

async def to_code(config, parent=None):
    var = cg.new_variable(config[CONF_ID], MirageM400TextSensor)
    await cg.register_component(var, config)
    
    if parent is None:
        # Fallback for standalone use
        parent = await cg.get_variable(config.get(CONF_MIRAGE_M400_ID))
    
    cg.add(parent.register_text_sensor(var))
    cg.add(var.set_parent(parent))
    
    await text_sensor.register_text_sensor(var, config)
