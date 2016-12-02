/*******************************************************************************
 System Interrupts File

  File Name:
    system_interrupt.c

  Summary:
    Raw ISR definitions.

  Description:
    This file contains a definitions of the raw ISRs required to support the
    interrupt sub-system.

  Summary:
    This file contains source code for the interrupt vector functions in the
    system.

  Description:
    This file contains source code for the interrupt vector functions in the
    system.  It implements the system and part specific vector "stub" functions
    from which the individual "Tasks" functions are called for any modules
    executing interrupt-driven in the MPLAB Harmony system.

  Remarks:
    This file requires access to the systemObjects global data structure that
    contains the object handles to all MPLAB Harmony module objects executing
    interrupt-driven in the system.  These handles are passed into the individual
    module "Tasks" functions to identify the instance of the module to maintain.
 *******************************************************************************/

// DOM-IGNORE-BEGIN
/*******************************************************************************
Copyright (c) 2011-2014 released Microchip Technology Inc.  All rights reserved.

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

#include <xc.h>
#include <sys/attribs.h>
#include "tsk_wifly_rx.h"
#include "tsk_wifly_tx.h"
#include "tsk_lfa_rx.h"
#include "system_definitions.h"
#include "public_vars.h"

// *****************************************************************************
// *****************************************************************************
// Section: System Interrupt Vector Functions
// *****************************************************************************
// *****************************************************************************

char uart0ByteRcvBuffer; // buffer to place received bytes in (uart0)
char uart1ByteRcvBuffer; // buffer to place received bytes in (uart1)

/* check variables for ISR queue posting 
    (used for debugger variable watch) */
int qSendCheckISR0;
int qSendCheckISR1;

void IntHandlerDrvUsartInstance0(void) {
    BaseType_t xHigherPriorityTaskWoken;

    /*check if there is data in the USART0 receive buffer*/
    if (PLIB_USART_ReceiverDataIsAvailable(USART_ID_1)) {

        /* set GPIO status to this interrupt */
        //sendGPIOStatus(STAT_INT_RX_UART0);

        /* get a byte from the queue */
        uart0ByteRcvBuffer = PLIB_USART_ReceiverByteReceive(USART_ID_1);

        /* put the byte in the receive queue */
        qSendCheckISR0 = xQueueSendToBackFromISR(wifly_rx_queue, &uart0ByteRcvBuffer, &xHigherPriorityTaskWoken);

        if (qSendCheckISR0 != pdTRUE) {
            sendGPIOError(ERR_BAD_MQ_SEND);
        }

    }

    DRV_USART_TasksTransmit(sysObj.drvUsart0);
    DRV_USART_TasksReceive(sysObj.drvUsart0);
    DRV_USART_TasksError(sysObj.drvUsart0);

    portEND_SWITCHING_ISR(xHigherPriorityTaskWoken)
}

void IntHandlerDrvUsartInstance1(void) {

    //    BaseType_t xHigherPriorityTaskWoken;
    //
    //    /*check if there is data in the USART0 receive buffer*/
    //    if (PLIB_USART_ReceiverDataIsAvailable (USART_ID_2))
    //    {
    //
    //      /* set GPIO status to this interrupt */
    //      //sendGPIOStatus(STAT_INT_RX_UART0);
    //      
    //      /* get a byte from the queue */
    //      uart1ByteRcvBuffer = PLIB_USART_ReceiverByteReceive (USART_ID_2);
    //
    //      /* put the byte in the receive queue */
    //      qSendCheckISR1 = xQueueSendToBackFromISR (lfa_rx_queue, &uart1ByteRcvBuffer, &xHigherPriorityTaskWoken);
    //
    //    }

    DRV_USART_TasksTransmit(sysObj.drvUsart1);
    DRV_USART_TasksReceive(sysObj.drvUsart1);
    DRV_USART_TasksError(sysObj.drvUsart1);

    //portEND_SWITCHING_ISR(xHigherPriorityTaskWoken)

}












/*******************************************************************************
 End of File
 */

