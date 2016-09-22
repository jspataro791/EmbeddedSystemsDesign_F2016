
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

APP_DATA appData;

#define UART_BUF_SIZE  32

// *****************************************************************************
// *****************************************************************************
// Section: Application Callback Functions
// *****************************************************************************
// *****************************************************************************

/* TODO:  Add any necessary callback functions.
*/

// *****************************************************************************
// *****************************************************************************
// Section: Application Local Functions
// *****************************************************************************
// *****************************************************************************

/* Write string to USART*/

char txbuffer[UART_BUF_SIZE];
DRV_USART_BUFFER_HANDLE tx_buff_handle;

void USART_WriteString(const DRV_HANDLE handle )
{
    DRV_USART_BufferAddWrite(handle, &tx_buff_handle, txbuffer, UART_BUF_SIZE );
}


// *****************************************************************************
// *****************************************************************************
// Section: Application Initialization and State Machine Functions
// *****************************************************************************
// *****************************************************************************

DRV_HANDLE testHandle;

void APP_Initialize ( void )
{
    /* Place the App state machine in its initial state. */
    appData.state = APP_STATE_INIT;

    /* Open the USART Driver */
    appData.appUsartHandle = DRV_USART_Open(sysObj.drvUsart0, DRV_IO_INTENT_READWRITE | DRV_IO_INTENT_NONBLOCKING);
    
     myRcvQueue = xQueueCreate((unsigned int)QLENGTH, sizeof(unsigned int));
    
     strcpy(txbuffer, "This is a test...\n\r");
     
}


// *****************************************************************************
// *****************************************************************************
// Section: Application Tasks
// *****************************************************************************
// *****************************************************************************

void APP_Tasks ( void )
{

    /* Check the application's current state. */
    switch ( appData.state )
    {
        /* Application's initial state. */
        case APP_STATE_INIT:
        {
            bool appInitialized = true;
            
            if(appInitialized)
            {
                appData.state = APP_STATE_TX;
            }
            
            break;
        }

                
        case APP_STATE_TX:
        {
            
         
                   USART_WriteString(appData.appUsartHandle);

            
            
            
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
