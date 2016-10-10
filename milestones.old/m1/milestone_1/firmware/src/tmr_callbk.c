#include "tmr_callbk.h"

void vTimerCallback1(TimerHandle_t xTimer)
{
       
    appData.timeEllapsed += 50;
    
    int goodSend = appSendTimerValToMQ(appData.appQHandle, appData.timeEllapsed);
    
    if(goodSend != true)
    {
        sendGPIOError(ERR_BAD_MQ_SEND);
    }
     
}
