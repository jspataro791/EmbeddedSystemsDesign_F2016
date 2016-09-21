
#include "debug.h"

void initGPIOError()
{
    PLIB_PORTS_DirectionOutputSet(PORTS_ID_0, ERR_GPIO_PORT, 0x00FF);
}

void sendGPIOError(uint8_t errCode)
{
    PLIB_PORTS_Write(PORTS_ID_0, ERR_GPIO_PORT, errCode);
    
    if(errCode != ERR_GOOD) {
        while(1) {}
    }
}