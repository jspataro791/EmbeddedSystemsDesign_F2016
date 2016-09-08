


// *****************************************************************************
// *****************************************************************************
// Section: Included Files 
// *****************************************************************************
// *****************************************************************************

#include "app.h"

// *****************************************************************************
// *****************************************************************************
// Section: Global Data Definitions
// *****************************************************************************
// *****************************************************************************

static uint8_t app_tx_buf[255];
static enum 
{
    USART_BM_INIT,
    USART_BM_WORKING,
    USART_BM_DONE,
} usartBMState;

/******************************************************************************
  Function:
    static void USART_Task (void)
    
   Remarks:
    Feeds the USART transmitter by reading characters from a specified pipe.  The pipeRead function is a 
    standard interface that allows data to be exchanged between different automatically 
    generated application modules.  Typically, the pipe is connected to the application's
    USART receive function, but could be any other Harmony module which supports the pipe interface. 
*/
static void USART_Task (void)
{
    switch (usartBMState)
    {
        default:
        case USART_BM_INIT:
        {
            appData.tx_count = 0;
            usartBMState = USART_BM_WORKING;
            break;
        }

        case USART_BM_WORKING:
        {
            
            /* Have we finished? */
            if (app_tx_buf[appData.tx_count] == '\0')
            {
                //usartBMState = USART_BM_INIT;
                appData.tx_count = 0;
            }
            
            if (appData.tx_count < sizeof(app_tx_buf)) 
            {
                if(!DRV_USART_TransmitBufferIsFull(appData.handleUSART0))
                {
                    DRV_USART_WriteByte(appData.handleUSART0, app_tx_buf[appData.tx_count]);
                    appData.tx_count++;
                }
            }
  
            break;
        }
    }
}

// *****************************************************************************
// *****************************************************************************
// Section: Application Initialization and State Machine Functions
// *****************************************************************************
// *****************************************************************************

/*******************************************************************************
  Function:
    void APP_Initialize ( void )

  Remarks:
    See prototype in app.h.
 */

void APP_Initialize ( void )
{
    /* Place the App state machine in its initial state. */
    appData.state = APP_STATE_INIT;
    
    // USART init
    appData.handleUSART0 = DRV_HANDLE_INVALID;
    
    // Error GPIO init
    initGPIOError();
    sendGPIOError(ERR_GOOD);
    
    // Set LED pin to out
    PLIB_PORTS_PinDirectionOutputSet(PORTS_ID_0, DBG_LED_PORT, DBG_LED_PIN);
      
    // Timer stuff
    
    appData.timerCount = 0;
    appData.timeEllapsed = 0;
    
    TimerHandle_t tmr1 = xTimerCreate("tmr1",
                                      pdMS_TO_TICKS(50),
                                      pdTRUE,
                                      (void*) 0,
                                      vTimerCallback1);
    
    if(tmr1 == NULL) // did the timer get created?
    {
        sendGPIOError(ERR_BAD_TIMER_INIT);
    }
    
    xTimerStart(tmr1, 0);
      
    // Initialize the timer queue
   QueueHandle_t  qH = appInitTimerMQ();
    
    if(qH == NULL) // did the queue init ok?
    {
        sendGPIOError(ERR_BAD_MQ_CREATE);
    }
    else // if so, set the app's queue handle
    {
        appData.appQHandle = qH;
    }
 
    
}


/******************************************************************************
  Function:
    void APP_Tasks ( void )

  Remarks:
    See prototype in app.h.
 */

void APP_Tasks ( void )
{

    /* Check the application's current state. */
    switch ( appData.state )
    {
        /* Application's initial state. */
        case APP_STATE_INIT:
        {
            bool appInitialized = true;
       
            if (appData.handleUSART0 == DRV_HANDLE_INVALID)
            {
                appData.handleUSART0 = DRV_USART_Open(APP_DRV_USART, DRV_IO_INTENT_READWRITE|DRV_IO_INTENT_NONBLOCKING);
                appInitialized &= ( DRV_HANDLE_INVALID != appData.handleUSART0 );
            }
        
            if (appInitialized)
            {
                /* initialize the USART state machine */
                usartBMState = USART_BM_INIT;
            
                appData.state = APP_STATE_SERVICE_TASKS;
            }
            break;
        }

        case APP_STATE_SERVICE_TASKS:
        {
                        
               unsigned int rcv; // msg Q copy buffer

		// block on message queue receive wait
               int rcvGood = xQueueReceive(appData.appQHandle, 
                                            (void*) &rcv,
                                            portMAX_DELAY);
               // Is the msg Q recv good?
               if(rcvGood != pdTRUE)
               {
                   // do error stuff
                   sendGPIOError(ERR_BAD_MQ_RECV);
               }
               
               // blink the LED for shits
               PLIB_PORTS_PinToggle(PORTS_ID_0, DBG_LED_PORT, DBG_LED_PIN);
               
               // USART stuff
               strcpy(app_tx_buf, PRINTNAMES); // copy print string into buffer
                              
               USART_Task(); // USART state machine
            
            break;
        }
        
        case APP_STATE_IDLE:
        {
            break;
        }
     

        /* The default state should never be executed. */
        default:
        {
            sendGPIOError(ERR_BAD_TASK_STATE);
            break;
        }
    }
}

 

/*******************************************************************************
 End of File
 */
