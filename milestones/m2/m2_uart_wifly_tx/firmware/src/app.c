
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

// USART stuff
uint8_t ubuffer[UART_BUF_SIZE];

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

int tx_count = 0; // used to keep track of transmit string position

USART_WriteString(const char * str, int numChar, const DRV_HANDLE handle )
{
    /* if the USART tx buffer is not full */
    if(!DRV_USART_TransmitBufferIsFull(handle)) {
        
        /* put a byte of the string in the buffer */
        DRV_USART_WriteByte(handle, str[tx_count]);
        
        /* increment the string position */
        tx_count++;
                
        /* if we reached the end of the string, reset*/
        if(tx_count == numChar) {
            tx_count = 0;
        }  
    }
              
}

// *****************************************************************************
// *****************************************************************************
// Section: Application Initialization and State Machine Functions
// *****************************************************************************
// *****************************************************************************

void APP_Initialize ( void )
{
    /* Place the App state machine in its initial state. */
    appData.state = APP_STATE_INIT;

    /* Open the USART Driver */
    appData.appUsartHandle = DRV_USART_Open(sysObj.drvUsart0, DRV_IO_INTENT_WRITE);
    
    char * testString = "This is a test. ";
    
    strcat(ubuffer, testString);
            
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
       
        
            if (appInitialized)
            {
            
                appData.state = APP_STATE_SERVICE_TASKS;
            }
            break;
        }

        case APP_STATE_SERVICE_TASKS:
        {
            USART_WriteString(ubuffer, UART_BUF_SIZE, appData.appUsartHandle);
            
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
