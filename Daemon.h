//
//  Daemon.h
//  
//
//  Created by Sudheeshna Karri on 4/26/17.
//
//

#ifndef Daemon_h
#define Daemon_h

//structures

struct arg_struct {
    int portno;
    int argc_main;
};

struct exec_arg_struct {
    int test_timeout;
    int test_loop;
};
struct buff {
    int a; //module ID
    float b; //Test ID
    char c[6]; //data type
    int d; //handle data size
    int e; // IsData
    //char f[16]; //filename
    int g; //Timeout
    char h[2]; //Data path
    int i; //loop count
    
}buffer;


//variables

char execution_command[4096];

pthread_mutex_t count_mutex     = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t  condition_var   = PTHREAD_COND_INITIALIZER;

char test_status[11];
char ack[18];
char result[4096];

// Functions


extern void* (test_execution)(void *arg1);

#endif /* Daemon_h */
