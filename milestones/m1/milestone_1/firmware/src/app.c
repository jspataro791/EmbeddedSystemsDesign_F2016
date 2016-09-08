/*******************************************************************************
  MPLAB Harmony Application Source File
  
  Company:
    Microchip Technology Inc.
  
  File Name:
    app.c

  Summary:
    This file contains the source code for the MPLAB Harmony application.

  Description:
    This file contains the source code for the MPLAB Harmony application.  It 
    implements the logic of the application's state machine and it may call 
    API routines of other MPLAB Harmony modules in the system, such as drivers,
    system services, and middleware.  However, it does not call any of the
    system interfaces (such as the "Initialize" and "Tasks" functions) of any of
    the modules in the system or make any assumptions about when those functions
    are called.  That is the responsibility of the configuration-specific system
    files.
 *******************************************************************************/

// DOM-IGNORE-BEGIN
/*******************************************************************************
Copyright (c) 2013-2014 released Microchip Technology Inc.  All rights reserved.

Microchip licenses to you the right to use, modify, copy and distribute
Software only when embedded on a Microchip microcontroller or digital signal
controller that is integrated into your product or third party product
(pursuant to the sublicense terms in the accompanying license agreement).

You should refer to the license agreement accompanying this Software for
additional information regarding your rights and obligations.

SOFTWARE AND DOCUMENTATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION, ANY WARRANTY OF
MERCHANTABILITY, TITLE, NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.
IN NO EVENT SHALL MICROCHIP OR ITS LICENSORS BE LIABLE OR OBLIGATED UNDER
CONTRACT, NEGLIGENCE, STRICT LIABILITY, CONTRIBUTION, BREACH OF WARRANTY, OR
OTHER LEGAL EQUITABLE THEORY ANY DIRECT OR INDIRECT DAMAGES OR EXPENSES
INCLUDING BUT NOT LIMITED TO ANY INCIDENTAL, SPECIAL, INDIRECT, PUNITIVE OR
CONSEQUENTIAL DAMAGES, LOST PROFITS OR LOST DATA, COST OF PROCUREMENT OF
SUBSTITUTE GOODS, TECHNOLOGY, SERVICES, OR ANY CLAIMS BY THIRD PARTIES
(INCLUDING BUT NOT LIMITED TO ANY DEFENSE THEREOF), OR OTHER SIMILAR COSTS.
 *******************************************************************************/
// DOM-IGNORE-END


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

// *****************************************************************************
/* Application Data

  Summary:
    Holds application data

  Description:
    This structure holds the application's data.

  Remarks:
    This structure should be initialized by the APP_Initialize function.
    
    Application strings and buffers are be defined outside this structure.
*/



static uint8_t app_tx_buf[255];
static enum 
{
    USART_BM_INIT,
    USART_BM_WORKING,
    USART_BM_DONE,
} usartBMState;

// *****************************************************************************
// *****************************************************************************
// Section: Application Callback Functions
// *****************************************************************************
// *****************************************************************************



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
// Section: Application Local Functions
// *****************************************************************************
// *****************************************************************************


/* Application's Timer Setup Function */


/* TODO:  Add any necessary local functions.
*/


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
            
            
            // main task loop, blocks on message recv
            //while(1)
            //{
               unsigned int rcv; // msg Q copy buffer
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
               strcpy(app_tx_buf, PRINTNAMES);
                              
               USART_Task();
               
          //  }
            
            break;
        }
        
        case APP_STATE_IDLE:
        {
            break;
        }

        /* TODO: implement your application state machine.*/
        

        /* The default state should never be executed. */
        default:
        {
            /* TODO: Handle error in application's state machine. */
            break;
        }
    }
}

 

/*******************************************************************************
 End of File
 */
