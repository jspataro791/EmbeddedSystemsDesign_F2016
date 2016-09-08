#include "app_public.h"

QueueHandle_t appInitTimerMQ()
    {
        return xQueueCreate((unsigned int)QLENGTH, sizeof(unsigned int));
    }

int appSendTimerValToMQ(QueueHandle_t q, unsigned int milliElapsed) 
    {
        return xQueueSend(q, &milliElapsed, portMAX_DELAY);
    }


