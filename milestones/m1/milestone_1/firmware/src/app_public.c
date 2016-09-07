#include "app_public.h"

QueueHandle_t appInitTimerMQ()
    {
        return xQueueCreate((unsigned int)QLENGTH, sizeof(unsigned int));
    }

int appSendTimerValToMQ(QueueHandle_t q, unsigned int milliElapsed) 
    {
        return xQueueSend(q, &milliElapsed, portMAX_DELAY);
    }

/*DRV_HANDLE usartInit()
{
        DRV_USART_INIT usartInit;
        SYS_MODULE_OBJ usartModule1;
        usartInit.baud = USART_BAUD;
        usartInit.flags = USART_FLAGS;
        usartInit.handshake = USART_HANDSHAKE;
        usartInit.interruptError = USART_INTERROR;
        usartInit.interruptReceive = USART_INTRECV;
        usartInit.interruptTransmit = USART_INTTRANS;
        usartInit.lineControl = USART_LINECONTROL;
        usartInit.mode = USART_MODE;
        usartInit.brgClock = USART_BRGCLOCK;
        usartInit.moduleInit.value = USART_MODULE_VALUE;
        usartInit.queueSizeReceive = USART_QUEUESIZERX;
        usartInit.queueSizeTransmit = USART_QUEUESIZETX;
        usartInit.usartID = USART_ID;
        usartModule1 = DRV_USART_Initialize(DRV_USART_0, (SYS_MODULE_INIT*)&usartInit);
        
        if(SYS_MODULE_OBJ_INVALID == usartModule1)
        {
            // do some error
        }
        
        SYS_INT_Initialize();
        SYS_INT_VectorPrioritySet(INT_VECTOR_USART2, INT_PRIORITY_LEVEL4);
        SYS_INT_VectorSubprioritySet(INT_VECTOR_UART2, INT_SUBPRIORITY_LEVEL0);
        SYS_INT_Enable();
        
        DRV_HANDLE usartHandle = DRV_USART_Open(DRV_USART_0, DRV_IO_INTENT_READWRITE | DRV_IO_INTENT_NONBLOCKING);
        
    }*/
    

