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

APP_DATA appData;
static uint8_t i2c_tx_buf[255];
static uint8_t i2c_rx_buf[255];
static uint8_t line_address = 0x3e;

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


/* TODO:  Add any necessary local functions.
*/
int initializeI2C()
{
    appData.lfa_address = &line_address;
    appData.i2cWriteBuffer = &i2c_rx_buf;
    appData.i2cReadBuffer = &i2c_rx_buf;
    
/*    DRV_I2C_INIT        i2c_init_data;

    i2c_init_data.i2cId = DRV_I2C_PERIPHERAL_ID_IDX0,
    i2c_init_data.i2cMode = DRV_I2C_MODE_MASTER,

    //Master mode parameters
    i2c_init_data.baudRate = 100000,
    i2c_init_data.busspeed = DRV_I2C_SLEW_RATE_CONTROL_IDX0,
    i2c_init_data.buslevel = DRV_I2C_SMBus_SPECIFICATION_IDX0,

    //interrupt sources
    i2c_init_data.mstrInterruptSource = INT_SOURCE_I2C_2_MASTER,
    i2c_init_data.slaveInterruptSource = INT_SOURCE_I2C_2_ERROR,
    i2c_init_data.errInterruptSource = INT_SOURCE_I2C_2_ERROR,
    i2c_init_data.queueSize = 1,

    //callback for Master (Master mode can use callbacks if needed)
    i2c_init_data.operationStarting = NULL,

    appData.i2cObjectHandle = DRV_I2C_Initialize(DRV_I2C_INDEX_0, (SYS_MODULE_INIT *)&i2c_init_data);
    if (SYS_MODULE_OBJ_INVALID == appData.i2cObjectHandle)
    {
        // Handle error
        return -1;
    }*/
    appData.i2cObjectHandle = sysObj.drvI2C0;
    
    if (DRV_I2C_Status(appData.i2cObjectHandle) != SYS_STATUS_READY)
    {
        // can't start doing reads and writes, nor can we open it yet
        return -1;
    }
    
    appData.i2cHandle = DRV_I2C_Open(I2C_ID_1, DRV_IO_INTENT_NONBLOCKING|DRV_IO_INTENT_READWRITE);
    if (DRV_HANDLE_INVALID == appData.i2cHandle)
    {
        // Handle open error
        return -1;
    }

    // turn on IR by writing byte 0x02 to REG_DATA_B (0x10)
    if (i2cWriteByte(0x10, 0x02))
    {
        appData.uart_tx_byte = '0';
        return - 1;
    }
        
    // turn on receiving by writing byte 0x00 to REG_DATA_B (0x10)
    if (i2cWriteByte(0x10, 0x00))
    {
        appData.uart_tx_byte = '1';
        return -1;
    }
    
    // Close the device when it is no longer needed.
    //DRV_I2C_Close(i2cObjectHandle);
    return 0;
}

int initializeUART()
{
    appData.uartHandle = DRV_USART_Open(APP_DRV_USART, DRV_IO_INTENT_READWRITE|DRV_IO_INTENT_NONBLOCKING);
    if (appData.uartHandle == DRV_HANDLE_INVALID)
    {
        return -1;
    }
    
}

char i2cBufferRead()
{
    DRV_I2C_BUFFER_EVENT my_event = DRV_I2C_TransferStatusGet(appData.i2cHandle, appData.i2cBufferHandle);
    while (1)
    {
        if (my_event == DRV_I2C_BUFFER_EVENT_ERROR)
        {
            appData.state = APP_STATE_FAILED;
            return -1;
        }else if (my_event != DRV_I2C_BUFFER_EVENT_COMPLETE)
        {
            continue;
        }else
            break;
    }
    // move received data into USART tx buffer
    /** TODO NEED TO FIGURE OUT FORMAT HERE*/
        
    // send data over USART
    appData.state = APP_STATE_TX;
}

char i2cWriteRead()
{         
            appData.i2cBufferHandle = DRV_I2C_BufferAddWriteRead( appData.i2cHandle,
                    appData.lfa_address, (I2C_DATA_TYPE *)&appData.i2cWriteBuffer[0], 
                    appData.i2cWriteSize, appData.i2cReadBuffer, appData.i2cReadSize, NULL );
            
            if (appData.i2cBufferHandle == NULL) {
                // Could not return a valid buffer handle.
                appData.state = APP_STATE_FAILED;
            }else {
                return i2cBufferRead();
            } 
}

int i2cReadByte(uint8_t address)
{
    appData.i2cBufferHandle = DRV_I2C_BufferAddRead(appData.i2cHandle, 
                                                address,
                                                &appData.i2cReadBuffer,
                                                appData.i2cReadSize,
                                                NULL);
    
    if (appData.i2cBufferHandle == NULL) 
    {
        // Could not return a valid buffer handle.
        appData.state = APP_STATE_FAILED;
        return -1;
    }
    
    DRV_I2C_BUFFER_EVENT my_event;
    while (1)
    {
        my_event = DRV_I2C_TransferStatusGet(appData.i2cHandle, appData.i2cBufferHandle);
        if (my_event == DRV_I2C_BUFFER_EVENT_ERROR)
        {
            appData.state = APP_STATE_FAILED;
            return -1;
        }else if (my_event != DRV_I2C_BUFFER_EVENT_COMPLETE)
        {
            continue;
        }else
            break;
    }
    return 0;
}

int i2cWriteByte(uint8_t address, uint8_t value)
{
    //(uint8_t)(*appData.i2cWriteBuffer) = value;
    i2c_tx_buf[0] = value;
    
    appData.i2cBufferHandle = DRV_I2C_BufferAddWrite(appData.i2cHandle, 
                                                &address,
                                                (I2C_DATA_TYPE *)&appData.i2cWriteBuffer[0],
                                                appData.i2cWriteSize,
                                                NULL);
    if (appData.i2cBufferHandle == NULL) 
    {
        // Could not return a valid buffer handle.
        appData.state = APP_STATE_FAILED;
        return -1;
    }
    
    DRV_I2C_BUFFER_EVENT my_event;
    while (1)
    {
        my_event = DRV_I2C_TransferStatusGet(appData.i2cHandle, appData.i2cBufferHandle);
        if (my_event == DRV_I2C_BUFFER_EVENT_ERROR)
        {
            appData.state = APP_STATE_FAILED;
            return -1;
        }else if (my_event != DRV_I2C_BUFFER_EVENT_COMPLETE)
        {
            continue;
        }else
            break;
    }
    
    return 0;
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

    
    /* TODO: Initialize your application's state machine and other
     * parameters.
     */
    /*
    if(initializeI2C() != 0)
    {
        appData.state = APP_STATE_FAILED;
    }*/
    
    if (initializeUART() != 0)
    {
        //appData.state = APP_STATE_FAILED;
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
           int appInitialized = 1;
        
            if (appInitialized)
            {
                appData.state = APP_STATE_I2C;
                
            }
           appData.state = APP_STATE_I2C;
            //appData.uart_tx_byte = 'S';
            //appData.state = APP_STATE_TX;
            //appData.state = APP_STATE_RX;
            break;
        }
        
        case APP_STATE_FAILED:
        {
            // failed to do something right, send message over UART
            appData.state = APP_STATE_TX;
            break;
        }

        /* TODO: implement your application state machine.*/
        case APP_STATE_RX:
        {
            if (!DRV_USART_ReceiverBufferIsEmpty(appData.uartHandle))
            {
               appData.uart_rx_byte = DRV_USART_ReadByte(appData.uartHandle); // read received byte
               appData.uart_tx_byte = appData.uart_rx_byte + 1;   // modifying received byte confirms it was received
               //appData.state = APP_STATE_TX;            // change state to TX
            }
            break;
        }

        /* TODO: implement your application state machine.*/
        case APP_STATE_TX:                              // USART transmit state
        {
            if(!DRV_USART_TransmitBufferIsFull(appData.uartHandle))
            {
                DRV_USART_WriteByte(appData.uartHandle, appData.uart_tx_byte);
                //appData.state = APP_STATE_RX;
                appData.state = APP_STATE_I2C;
                break;
            }
            break;
        }

        case APP_STATE_I2C:
        {
            // read byte from REG_DATA_A (0x11)
            if (i2cReadByte(0x11))
            {
                appData.uart_tx_byte = '2';
                appData.state = APP_STATE_TX;
                break;
            }
            
            appData.uart_tx_byte = i2c_rx_buf[0];
            appData.state = APP_STATE_TX;
            break;
        }
        
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
