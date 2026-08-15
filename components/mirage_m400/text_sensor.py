import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor
from esphome.const import CONF_ID, CONF_NAME

from . import mirage_m400_ns, MirageM400Component

DEPENDENCIES = ["mirage_m400"]

MirageTextSensor = mirage_m400_ns.class_(
    "MirageTextSensor", text_sensor.TextSensor, cg.Component
)

CONFIG_SCHEMA = text_sensor.TEXT_SENSOR_SCHEMA.extend(
    {
        cv.GenerateID(): cv.declare_id(MirageTextSensor),
        cv.GenerateID("mirage_m400_id"): cv.use_id(MirageM400Component),
    }
)


async def to_code(config):
    parent = await cg.get_variable(config["mirage_m400_id"])
    var = cg.new_Pvariable(config[CONF_ID], parent)
    await text_sensor.register_text_sensor(var, config)
    await cg.register_component(var, config)
