#include "tsk_motorctrl.h"
#include "system_definitions.h"
#include "rvr_config.h"

void initMotorPins()
{
    /* enable = output */
    PLIB_PORTS_DirectionOutputSet(PORTS_ID_0, MOTOR_ENABLE_PORT, MOTOR_ENABLE_PIN);
    
    /* directions = output*/
    PLIB_PORTS_DirectionOutputSet(PORTS_ID_0, MOTOR1_DIR_PORT, MOTOR1_DIR_PIN);
    PLIB_PORTS_DirectionOutputSet(PORTS_ID_0, MOTOR2_DIR_PORT, MOTOR2_DIR_PIN);
}

void StopMotors()
{
    /* enable = disabled*/
    PLIB_PORTS_Clear(PORTS_ID_0, MOTOR_ENABLE_PORT, MOTOR_ENABLE_PIN);
    
 }

void ForwardMotors()
{
    /* enable = enabled*/
    PLIB_PORTS_Write(PORTS_ID_0, MOTOR_ENABLE_PORT, MOTOR_ENABLE_PIN);
    
    /* directions = forward*/
    PLIB_PORTS_Clear(PORTS_ID_0, MOTOR1_DIR_PORT, MOTOR1_DIR_PIN);
    PLIB_PORTS_Clear(PORTS_ID_0, MOTOR2_DIR_PORT, MOTOR2_DIR_PIN);
}

void ReverseMotors()
{
    /* enable = enabled*/
    PLIB_PORTS_Write(PORTS_ID_0, MOTOR_ENABLE_PORT, MOTOR_ENABLE_PIN);
    
    /* directions = forward*/
    PLIB_PORTS_Write(PORTS_ID_0, MOTOR1_DIR_PORT, MOTOR1_DIR_PIN);
    PLIB_PORTS_Write(PORTS_ID_0, MOTOR2_DIR_PORT, MOTOR2_DIR_PIN);
}

void LeftMotors()
{
    /* enable = enabled*/
    PLIB_PORTS_Write(PORTS_ID_0, MOTOR_ENABLE_PORT, MOTOR_ENABLE_PIN);
    
    /* directions = left*/
    PLIB_PORTS_Clear(PORTS_ID_0, MOTOR1_DIR_PORT, MOTOR1_DIR_PIN);
    PLIB_PORTS_Write(PORTS_ID_0, MOTOR2_DIR_PORT, MOTOR2_DIR_PIN);
}

void RightMotors()
{
    /* enable = enabled*/
    PLIB_PORTS_Write(PORTS_ID_0, MOTOR_ENABLE_PORT, MOTOR_ENABLE_PIN);
    
    /* directions = left*/
    PLIB_PORTS_Write(PORTS_ID_0, MOTOR1_DIR_PORT, MOTOR1_DIR_PIN);
    PLIB_PORTS_Clear(PORTS_ID_0, MOTOR2_DIR_PORT, MOTOR2_DIR_PIN);
}

void MOTOR_CTRL_Initialize()
{
        initMotorPins();
        StopMotors();
}

void MOTOR_CTRL_Tasks()
{
    vTaskDelay(10000);
}