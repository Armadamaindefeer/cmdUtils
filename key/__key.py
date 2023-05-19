from .__key_common import *
import os

if os.name == 'nt':
	from .__key_ms import *
else:
	from .__key_posix import *


forbidden_key = {

# common
CR,
ESC,
#key.TAB,
INSERT,
SUPR,
HOME,
END,
PAGE_UP,
PAGE_DOWN,
DELETE,

# CTRL
CTRL_A,CTRL_B,CTRL_D,CTRL_E,
CTRL_F,CTRL_G,CTRL_H,
CTRL_K,CTRL_L,CTRL_M,CTRL_N,CTRL_O,
CTRL_P,CTRL_Q,CTRL_R,CTRL_S,CTRL_T,
CTRL_U,CTRL_V,CTRL_W,CTRL_X,CTRL_Y,
CTRL_Z,

# Cursor
LEFT,
RIGHT,

# Function
F1,F2,F3,
F4,F5,F6,
F7,F8,F9,
F10,F11,F12

#Other
#key.SHIFT_TAB,
#key.CTRL_ALT_SUPR,
#key.ALT_A,
#key.CTRL_ALT_A
}
