import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import button, number
from esphome.const import CONF_ID

from . import mirage_m400_ns

CONF_VOLUME_ID = "volume_id"
CONF_STEP = "step"

MirageVolumeButton = mirage_m400_ns.class_(
    "MirageVolumeButton", button.Button, cg.Component
)
MirageVolumeUpButton = mirage_m400_ns.class_("MirageVolumeUpButton", MirageVolumeButton)
MirageVolumeDownButton = mirage_m400_ns.class_("MirageVolumeDownButton", MirageVolumeButton)

BASE_SCHEMA = cv.Schema(
    {
        # References the "id:" of the MirageVolumeNumber entity (see number.py)
        # this button should step up/down.
        cv.Required(CONF_VOLUME_ID): cv.use_id(number.Number),
        cv.Optional(CONF_STEP, default=5): cv.int_range(min=1, max=160),
    }
).extend(cv.COMPONENT_SCHEMA)

# The "type:" key selects which MirageVolumeButton subclass gets instantiated,
# mirroring the pattern used by switch.py's power/mute types.
CONFIG_SCHEMA = cv.typed_schema(
    {
        "volume_up": button.button_schema(MirageVolumeUpButton).extend(BASE_SCHEMA),
        "volume_down": button.button_schema(MirageVolumeDownButton).extend(BASE_SCHEMA),
    },
    lower=True,
)


async def to_code(config):
    volume_number = await cg.get_variable(config[CONF_VOLUME_ID])
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await button.register_button(var, config)
    cg.add(var.set_number(volume_number))
    cg.add(var.set_step(config[CONF_STEP]))
