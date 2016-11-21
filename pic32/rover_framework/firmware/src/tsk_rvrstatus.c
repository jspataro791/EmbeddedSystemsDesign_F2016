#include "tsk_rvrstatus.h"
#include "debug.h"
#include "public_vars.h"


char rvrStatusBuffer[MAX_QUEUE_ITEM_SIZE];

void RVRStatus_Initialize()
{
    sendGPIOStatus(STAT_RVRSTATUS_INIT);
}

void RVRStatus_Tasks()
{
    sendGPIOStatus(STAT_RVRSTATUS_TASK_ENTER);
    
    int QRcvChk = xQueueReceive( valid_data_queue, &rvrStatusBuffer, portMAX_DELAY );
    
    if(QRcvChk == pdTRUE)
    {
        /* get index of D */
        int index = 0;
        for(index; index < strlen(rvrStatusBuffer);index++)
        {
            if(rvrStatusBuffer[index] == 'D')
            {
                break;
            }
        }
        
        RVR_CurDirection = rvrStatusBuffer[index + 1];
        
        /* get index of S */
        index = 0;
        for(index; index < strlen(rvrStatusBuffer);index++)
        {
            if(rvrStatusBuffer[index] == 'S')
            {
                break;
            }
        }
        
        RVR_CurSpeed = rvrStatusBuffer[index + 1];
        
        sendDirStatus((uint8_t)RVR_CurDirection);
        sendSpdStatus((uint8_t)RVR_CurSpeed);
        
    }
    else
    {
        sendGPIOError(ERR_BAD_MQ_RECV);
    }
}
