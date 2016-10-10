
// *****************************************************************************
// *****************************************************************************
// Section: Included Files
// *****************************************************************************
// *****************************************************************************

#include "system_config.h"
#include "system_definitions.h"
#include "uartrcv.h"
#include "uarttrans.h"
#include "uartloopback.h"
#include "heartbeat.h"


// *****************************************************************************
// *****************************************************************************
// Section: Local Prototypes
// *****************************************************************************
// *****************************************************************************


 
static void _SYS_Tasks ( void );
static void _UARTRCV_Tasks(void);
static void _UARTTRANS_Tasks(void);
static void _UARTLOOPBACK_Tasks(void);
static void _DEBUG_GENERATOR_Tasks(void);


// *****************************************************************************
// *****************************************************************************
// Section: System "Tasks" Routine
// *****************************************************************************
// *****************************************************************************

/*******************************************************************************
  Function:
    void SYS_Tasks ( void )

  Remarks:
    See prototype in system/common/sys_module.h.
*/

void SYS_Tasks ( void )
{
    /* Create OS Thread for Sys Tasks. */
//    xTaskCreate((TaskFunction_t) _SYS_Tasks,
//                "Sys Tasks",
//                1024, NULL, 1, NULL);
    
    sendGPIOStatus(STAT_SYS_TASK_CREATE);

    /* Create OS Thread for UARTRCV Tasks. */
    xTaskCreate((TaskFunction_t) _UARTRCV_Tasks,
                "UARTRCV Tasks",
                1024, NULL, 1, NULL);
    
    /* Create OS Thread for UARTTRANS Tasks. */
    xTaskCreate((TaskFunction_t) _UARTTRANS_Tasks,
                "UARTTRANS Tasks",
                1024, NULL, 1, NULL);

    /* Create OS Thread for UARTLOOPBACK Tasks. */
    /*xTaskCreate((TaskFunction_t) _UARTLOOPBACK_Tasks,
                "UARTLOOPBACK Tasks",
                1024, NULL, 1, NULL);*/
    
    /* Create OS Thread for DEBUG_GENERATOR Tasks. */
    xTaskCreate((TaskFunction_t) _DEBUG_GENERATOR_Tasks,
                "DEBUG GENERATOR Tasks",
                1024, NULL, 1, NULL);

    /**************
     * Start RTOS * 
     **************/
    vTaskStartScheduler(); /* This function never returns. */
}


/*******************************************************************************
  Function:
    void _SYS_Tasks ( void )

  Summary:
    Maintains state machines of system modules.
*/
static void _SYS_Tasks ( void)
{
    while(1)
    {
        /* Maintain system services */
        SYS_DEVCON_Tasks(sysObj.sysDevcon);

        /* Maintain Device Drivers */

        /* Maintain Middleware */

        /* Task Delay */
    }
}


/*******************************************************************************
  Function:
    void _UARTRCV_Tasks ( void )

  Summary:
    Maintains state machine of UARTRCV.
*/

static void _UARTRCV_Tasks(void)
{
    while(1)
    {
        UARTRCV_Tasks();
    }
}


/*******************************************************************************
  Function:
    void _UARTTRANS_Tasks ( void )

  Summary:
    Maintains state machine of UARTTRANS.
*/

static void _UARTTRANS_Tasks(void)
{
    while(1)
    {
        UARTTRANS_Tasks();
    }
}


/*******************************************************************************
  Function:
    void _UARTLOOPBACK_Tasks ( void )

  Summary:
    Maintains state machine of UARTLOOPBACK.
*/

static void _UARTLOOPBACK_Tasks(void)
{
    while(1)
    {
        UARTLOOPBACK_Tasks();
    }
}

/*******************************************************************************
  Function:
    void _DEBUG_GENERATOR_Tasks ( void )

  Summary:
    Maintains state machine of UARTLOOPBACK.
*/

static void _DEBUG_GENERATOR_Tasks(void)
{
    while(1)
    {
        HEARTBEAT_Tasks();
    }
}


/*******************************************************************************
 End of File
 */

