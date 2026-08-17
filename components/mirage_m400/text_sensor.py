import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor
from . import mirage_m400

DEPENDENCIES = ['mirage_m400']

CONFIG_SCHEMA = cv.Schema({
    cv.Optional(text_sensor.TEXT_SENSOR_ID): cv.generate_id(),
}).extend(text_sensor.CONFIG_SCHEMA)

async def to_code(config):
    cg = cg.get_variable(cv.get_id(config))
    # FIXED: Added 'new' and parentheses
    cg.add_literal(cg.MirageM400TextSensor())
    # Wait, the correct way in ESPHome is usually:
    # var = cg.add_new_sig(cg.MirageM400TextSensor())
    # But for a basic custom component:
    hub = cg.get_variable(cv.get_id(mirage_m400.CONF_MIRAGE_M400_ID))
    cg.register_component(cg.MirageM400TextSensor(), config)
    # Correct implementation for a custom entity:
    sensor = cg.new_Pvariable(cg.MirageM400TextSensor())
    cg.add_expression(" %s->set_parent(%s);" % (sensor, hub))
    cg.add_expression(" %s->register_text_sensor(%s);" % (hub, sensor))
    cg.register_text_sensor(sensor, config)
