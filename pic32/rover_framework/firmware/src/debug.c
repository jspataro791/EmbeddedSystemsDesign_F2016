#include "debug.h"

void initGPIODebug()
{
    PLIB_PORTS_DirectionOutputSet(PORTS_ID_0, ERR_GPIO_PORT, 0x00FF);
}

void sendGPIOError(uint8_t errCode)
{
    PLIB_PORTS_Write(PORTS_ID_0, ERR_GPIO_PORT, errCode);
    
    if(errCode != ERR_GOOD) {
        
        vTaskSuspendAll();
        while(1) {}
    }
}

void sendGPIOStatus(uint8_t stat)
{
    PLIB_PORTS_Write(PORTS_ID_0, ERR_GPIO_PORT, stat);
}
