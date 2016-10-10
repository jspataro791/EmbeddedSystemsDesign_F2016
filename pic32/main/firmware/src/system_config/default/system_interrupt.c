
// *****************************************************************************
// *****************************************************************************
// Section: Included Files
// *****************************************************************************
// *****************************************************************************

#include <xc.h>
#include <sys/attribs.h>
#include "uartrcv.h"
#include "uarttrans.h"
#include "uartloopback.h"
#include "system_definitions.h"
#include "queue.h"

// *****************************************************************************
// *****************************************************************************
// Section: System Interrupt Vector Functions
// *****************************************************************************
// *****************************************************************************

extern QueueHandle_t uart0RcvQueue; // Externally defined receive queue
char uart0ByteRcvBuffer; // buffer to place received bytes in
int SendChkISR; // used to debug whether message was sent to queue correctly

/* USART driver interrupt handler */
void
IntHandlerDrvUsartInstance0 (void)
{
  BaseType_t xHigherPriorityTaskWoken;

  /*check if there is data in the USART0 receive buffer*/
  if (PLIB_USART_ReceiverDataIsAvailable (USART_ID_1))
    {

      /* set GPIO status to this interrupt */
      sendGPIOStatus(STAT_INT_RX_UART0);
      
      /* get a byte from the queue */
      uart0ByteRcvBuffer = PLIB_USART_ReceiverByteReceive (USART_ID_1);

      /* put the byte in the receive queue */
      SendChkISR = xQueueSendToBackFromISR (uart0RcvQueue, &uart0ByteRcvBuffer, &xHigherPriorityTaskWoken);

    }

  /* these clear flags and stuff, idk */
  DRV_USART_TasksTransmit (sysObj.drvUsart0);
  DRV_USART_TasksReceive (sysObj.drvUsart0);
  DRV_USART_TasksError (sysObj.drvUsart0);

}














/*******************************************************************************
 End of File
 */

