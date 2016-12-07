/* 
 * File:   tsk_lfa_decision.h
 * Author: john
 *
 * Created on December 4, 2016, 1:31 PM
 */

#ifndef TSK_LFA_DECISION_H
#define	TSK_LFA_DECISION_H

#ifdef	__cplusplus
extern "C" {
#endif

	typedef enum {
		/* line following*/
		STRAIGHT,

		/* intersection detection */
		LEFT_TURN,
		RIGHT_TURN,
		TWOWAY_TURN,
		TURN_STAGING,
		TURN_EXECUTE,
		TURN_FINISH_LEFT,
		TURN_FINISH_RIGHT,
                TURN_STRAIGHTEN


	} LFA_DECISION_STATES;

	typedef struct {
		LFA_DECISION_STATES decState;


	} LFA_DECISION_DATA;

	void LFA_DECISION_Initialize();
	void LFA_DECISION_Tasks();



#ifdef	__cplusplus
}
#endif

#endif	/* TSK_LFA_DECISION_H */

