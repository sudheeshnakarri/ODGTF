//
//  Daemon.c
//
//
//  Created by Sudheeshna Karri on 4/1/17.
//
//TODO:
//Need to define proper buffer sizes
//Implement user execution termination
//Different thread for result
//Recieve data structure and directly assign it to structure in C
//Use all the structure variables to handle the process.
//

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#define NUM_THREADS     3
#define die(e) do { fprintf(stderr, "%s\n", e); exit(EXIT_FAILURE); } while (0);


void error(const char *msg)
{
    perror(msg);
    exit(1);
}

//global variables
struct arg_struct {
    int portno;
    int argc_main;
};
char buffer[4096];
char execution_command[4096];
char test_status[11];
char ack[18];
char result[11];

pthread_mutex_t count_mutex     = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t  condition_var   = PTHREAD_COND_INITIALIZER;

//***** Function to handle the test execution ********

void *test_execution()
{
    
    //add while loop to handle longer execution time
    //should I use execl(),pipe(),fork() etc ??instead  Ask
    FILE *fp = popen(execution_command, "r");
    sleep(5);
    fgets(result, 11 , fp);
    pclose(fp);
    
    pthread_detach(pthread_self());
    printf("Result: %s\n",result);
    // Send back read data using 'result' , its global variable
    strcpy(test_status,"DONE EXECUTION");
    pthread_exit(NULL);
}


//********** TCP Communication *****************

void *tcp_connection( void *arguments )
{
    struct arg_struct *args = arguments;
    int portid,argc_check;

    portid = args->portno;
    argc_check = args->argc_main;
    
    if (argc_check < 2) {
        fprintf(stderr,"ERROR, no port provided\n");
        exit(1);
    }
    
    printf( "I am fine\n" );
    int sockfd, newsockfd;
    socklen_t clilen;
    struct sockaddr_in serv_addr, cli_addr;
    bzero(execution_command,4096);
    int n;
    //handling threads : Result thread and execution thread
    pthread_t internal_threads[ 2 ];
    int result_code;
    
   
    
        //socket creation
        
        sockfd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
        if (sockfd < 0)
            error("ERROR opening socket");
        bzero((char *) &serv_addr, sizeof(serv_addr));
        
        serv_addr.sin_family = AF_INET;
        serv_addr.sin_addr.s_addr = INADDR_ANY;
        serv_addr.sin_port = htons(portid);
        
        
        //socket binding
        
        if (bind(sockfd, (struct sockaddr *) &serv_addr,
                 sizeof(serv_addr)) < 0)
            error("ERROR on binding");
        
        
        // socket listening
        
        listen(sockfd,5);
        clilen = sizeof(cli_addr);
        int notdone =1;
    
    
    //adding 'while' to keep server running
    
    while (notdone) {
        
        //accept connections
        newsockfd = accept(sockfd,
                               (struct sockaddr *) &cli_addr,
                               &clilen);
        if (newsockfd < 0)
            error("ERROR on accept");
        
        bzero(buffer,4096);
        n = read(newsockfd,buffer,4096);
        if (n < 0) error("ERROR reading from socket");
        printf("Here is the message: %s\n",buffer);
        
        
        //handling status
        if(strcmp(buffer,"Status")== 0){
            
            n = write(newsockfd,test_status,sizeof(test_status));
            if (n < 0) error("ERROR writing to socket");
           
            close(newsockfd);
        
        }
        else if (strcmp(buffer,"Result")== 0) {
            n = write(newsockfd,result,sizeof(result)-1);
             if (n < 0) error("ERROR writing to socket");
            close(newsockfd);
        }
        else {
                strcpy(test_status,"IN PROGRESS");
                strcpy(execution_command,buffer);
                strcpy(ack,"TEST CASE Recieved");
                n = write(newsockfd,ack,sizeof(ack));
            if (n < 0) error("ERROR writing to socket");

            // Creating thread for test execution , this will detach itself after execution
                result_code = pthread_create( &internal_threads[0], NULL, test_execution, NULL);
                assert( !result_code );
            
            close(newsockfd);
            }
            
            
        }
   
    close(sockfd);
    
    return NULL;
}

// Main function

int main( int argc, char *argv[] )
{
    
    if (argc < 2) {
        fprintf(stderr,"ERROR, no port provided\n");
        exit(1);
    }
    
    pthread_t threads[ NUM_THREADS ];
    int result_code;
    unsigned index;
    
    
    struct arg_struct thread_args;
    thread_args.portno = atoi(argv[1]);
    thread_args.argc_main=argc;
    
    
    // create Communicatin thread
    
    result_code = pthread_create( &threads[0], NULL, tcp_connection,&thread_args );
    assert( !result_code );
    
    // wait for communication thread to complete
    result_code = pthread_join( threads[0], NULL );
    assert( !result_code );
    
    printf( "In main: All threads completed successfully\n" );
    exit( EXIT_SUCCESS );
}
