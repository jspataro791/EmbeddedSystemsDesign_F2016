/* This file includes a custom initialization routine. 
   All new init stuff should go in this and be injected into
  the SYS_Init() routine.*/

#ifndef CUSTOM_INIT_H
#define	CUSTOM_INIT_H

#include "public_vars.h"

void initPublicQueues();
void initRvrStatus();


#endif	/* CUSTOM_INIT_H */

