//
//  test_execution.c
//  
//
//  Created by Sudheeshna Karri on 4/26/17.
//
//

#include <stdio.h>
#include "Daemon.h"

// execution thread

void *test_execution(void *execution_args)
{
    struct exec_arg_struct *execution_arguments= execution_args;
    int TIMEOUT, LOOP;
    TIMEOUT = execution_arguments->test_timeout;
    LOOP = execution_arguments->test_loop;
    
    
    //add while loop to it
    FILE *fp = popen(execution_command, "r");
    if (fp == NULL) {
        printf("Failed to run command\n" );
        exit(1);
    }
    //sleep(5);
    if (fp != NULL) {
        
        //Timeout implementation : Need to be improved
        time_t startTime = time(NULL);
        
        // should improve fget NULL ,write into a file
        while (1) {
            if(time(NULL) - startTime > 3) break;
            //  printf("\ntime  diff %ld \n",(time(NULL) - startTime));
            char *line;
            line = fgets(result, 4096 , fp);
            if (line == NULL) break;
            // if (line[0] == 'd') printf("%s", line); /* line includes '\n' */
            
        }
    }
    
    //fgets(result, 4096 , fp);
    if (pclose(fp) == -1) {
        fprintf(stderr,"ERROR, reported by pclose()");
    } else {
        /* Use macros described under wait() to inspect `status' in order
         to determine success/failure of command executed by popen() */
        
    }
    
    
    pthread_detach(pthread_self());
    //printf("Result: %s\n",result);
    // Send back the result
    //n = write(newsockfd,result,sizeof(result)-1);
    strcpy(test_status,"DONE EXECUTION");
    pthread_exit(NULL);
}



