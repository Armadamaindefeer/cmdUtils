from .readchar import key

forbidden_key = {

# common
key.CR,
key.ESC,
key.TAB,
key.INSERT,
key.SUPR,
key.HOME,
key.END,
key.PAGE_UP,
key.PAGE_DOWN,

# CTRL
key.DELETE,
key.CTRL_A,key.CTRL_B,key.CTRL_D,key.CTRL_E,
key.CTRL_F,key.CTRL_G,key.CTRL_H,key.CTRL_I,
key.CTRL_K,key.CTRL_L,key.CTRL_M,key.CTRL_N,key.CTRL_O,
key.CTRL_P,key.CTRL_Q,key.CTRL_R,key.CTRL_S,key.CTRL_T,
key.CTRL_U,key.CTRL_V,key.CTRL_W,key.CTRL_X,key.CTRL_Y,
key.CTRL_Z,

# Cursor
key.LEFT,
key.RIGHT,

# Function
key.F1,key.F2,key.F3,
key.F4,key.F5,key.F6,
key.F7,key.F8,key.F9,
key.F10,key.F11,key.F12

#Other
#key.SHIFT_TAB,
#key.CTRL_ALT_SUPR,
#key.ALT_A,
#key.CTRL_ALT_A

}
