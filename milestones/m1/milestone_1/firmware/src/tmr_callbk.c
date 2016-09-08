#include "tmr_callbk.h"

void vTimerCallback1(TimerHandle_t xTimer)
{
       
    appData.timeEllapsed += 50;
    
    int goodSend = appSendTimerValToMQ(appData.appQHandle, appData.timeEllapsed);
    
    if(goodSend != true)
    {
        //PLIB_PORTS_PinToggle(PORTS_ID_0, DBG_LED_PORT, DBG_LED_PIN);
    }
     
}
