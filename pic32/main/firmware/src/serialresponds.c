#include "serialresponds.h"
#include "system_definitions.h"
#include "queue.h"

extern QueueHandle_t uart0TransQueue;

void serial0Respond(char * resp)
{
    int i = 0;
    for(i; i < sizeof(resp); i++)
    {
       xQueueSend(uart0TransQueue, &resp[i], 0); 
    }
    
}
