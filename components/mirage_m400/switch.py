import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from esphome.const import CONF_ID

from . import CONF_MIRAGE_M400_ID, MirageM400Component, mirage_m400_ns

CONF_ZONE = "zone"

MirageSwitch = mirage_m400_ns.class_("MirageSwitch", switch.Switch, cg.Component)
MirageStandbySwitch = mirage_m400_ns.class_("MirageStandbySwitch", MirageSwitch)
MirageMuteSwitch = mirage_m400_ns.class_("MirageMuteSwitch", MirageSwitch)

BASE_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_MIRAGE_M400_ID): cv.use_id(MirageM400Component),
        cv.Required(CONF_ZONE): cv.int_range(min=1, max=32),
    }
).extend(cv.COMPONENT_SCHEMA)

# The "type:" key selects which MirageSwitch subclass gets instantiated. Using
# cv.typed_schema means each branch declares its own id with the right C++ type,
# so codegen emits the subclass directly.
CONFIG_SCHEMA = cv.typed_schema(
    {
        "power": switch.switch_schema(MirageStandbySwitch).extend(BASE_SCHEMA),
        "mute": switch.switch_schema(MirageMuteSwitch).extend(BASE_SCHEMA),
    },
    lower=True,
)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_MIRAGE_M400_ID])
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await switch.register_switch(var, config)
    cg.add(var.set_parent(parent))
    cg.add(var.set_zone(config[CONF_ZONE]))
