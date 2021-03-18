from string import Template

templateString = Template(
"""#ifndef $MACRO_GUARD
#define $MACRO_GUARD

#include "$ICON_HEADER_PATH"
    
const Icon STATIC_SECTION $ARRAY_NAME = {$ICON_WIDTH, $ICON_HEIGHT, (const uint8_t[]){$ICON_DATA}};
    
#endif"""
) 