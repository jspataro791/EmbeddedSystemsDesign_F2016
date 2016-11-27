#include "tsk_motorctrl.h"
#include "system_definitions.h"
#include "rvr_config.h"
#include "public_vars.h"

void InitMotorPins()
{
     /* set chipkit pin 3 (RD0) to output */
    TRISDbits.TRISD0 = 0;
    
    /* set chipkit pin 4 (RC14) to output */
    TRISCbits.TRISC14 = 0;
    
    /* set chipkit pin 78 (RG1) to output */
    TRISGbits.TRISG1 = 0;
}

void StopMotors()
{
    /* enable = disabled*/
    PORTDbits.RD0 = 0;
 }

void ForwardMotors()
{
    /* enable = disabled*/
    PORTDbits.RD0 = 1;
    
    /* motor1 = forward */
    PORTCbits.RC14 = 0;
    /* motor2 = forward */
    PORTGbits.RG1 = 0;
}

void ReverseMotors()
{
    /* enable = disabled*/
    PORTDbits.RD0 = 1;
    
    /* motor1 = reversed */
    PORTCbits.RC14 = 1;
    /* motor2 = reversed */
    PORTGbits.RG1 = 1;
}

void LeftMotors()
{
    /* enable = disabled*/
    PORTDbits.RD0 = 1;
    
    /* motor1 = forward */
    PORTCbits.RC14 = 0;
    /* motor2 = reversed */
    PORTGbits.RG1 = 1;
}

void RightMotors()
{
    /* enable = disabled*/
    PORTDbits.RD0 = 1;
    
    /* motor1 = reversed */
    PORTCbits.RC14 = 1;
    /* motor2 = forward */
    PORTGbits.RG1 = 0;
}

void MOTOR_CTRL_Initialize()
{
    
    /* send task enter debug status */
    sendGPIOStatus(STAT_MTR_CTRL_INIT);
        
    /* init and stop motors*/
        InitMotorPins();
        StopMotors();
}

char mtrCtrlBuffer;

void MOTOR_CTRL_Tasks()
{
     /* send task enter debug status */
    sendGPIOStatus(STAT_MTR_CTRL_TASK_ENTER);
    
    /* block until data received on transmit queue */
    int QRcvChk = xQueueReceive( motor_ctrl_queue, &mtrCtrlBuffer, portMAX_DELAY );

    /* if queue rcv was successful */
    if ( QRcvChk == pdTRUE ) {
        
        if (mtrCtrlBuffer == 'L')
        {
            LeftMotors();
        }
        else if(mtrCtrlBuffer == 'R')
        {
            RightMotors();
        }
        else if(mtrCtrlBuffer == 'S')
        {
            ForwardMotors();
        }
        else if (mtrCtrlBuffer == 'B')
        {
            ReverseMotors();
        }   
    }
    else
    {
        sendGPIOError(ERR_BAD_MQ_RECV);
    }
}