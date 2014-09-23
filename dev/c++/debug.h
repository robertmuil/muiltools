#ifndef __debug_h
#define __debug_h

#define out(s,...) printf(s ,##__VA_ARGS__)

#if DBG_LVL > 0
#define dbg(x,s,...) if(DBG_LVL>=x)out(s ,##__VA_ARGS__)
#else
#define dbg(x,s,...)
#endif


#endif /* __debug_h */
