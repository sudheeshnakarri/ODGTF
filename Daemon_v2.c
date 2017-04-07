//
//  threads.c
//
//
//  Created by Sudheeshna Karri on 4/1/17.
//
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

struct arg_struct {
    int portno;
    int argc_main;
};
//global variables

char buffer[4096];

char execution_command[4096];

pthread_mutex_t count_mutex     = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t  condition_var   = PTHREAD_COND_INITIALIZER;

char test_status[11];
char ack[18];
char result[11];
//strcpy(test_status,"NA");

void *test_execution()
{
    
    
    FILE *fp = popen(execution_command, "r");
    sleep(5);
    fgets(result, 11 , fp);
    pclose(fp);
    
    pthread_detach(pthread_self());
    //printf("Result: %s\n",result);
    // Send back the result
    //n = write(newsockfd,result,sizeof(result)-1);
    strcpy(test_status,"DONE EXECUTION");
    pthread_exit(NULL);
}





void *tcp_connection( void *arguments )
{
    struct arg_struct *args = arguments;
    
    int sockfd, newsockfd, portid,argc_check;
    portid = args->portno;
    argc_check = args->argc_main;
    socklen_t clilen;
    int n;
    //handling threads
    pthread_t internal_threads[ 2 ];
    int result_code;
    bzero(execution_command,4096);
    
    struct sockaddr_in serv_addr, cli_addr;
    
    if (argc_check < 2) {
        fprintf(stderr,"ERROR, no port provided\n");
        exit(1);
    }
    
    //socket creation
    
    
    sockfd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sockfd < 0)
        error("ERROR opening socket");
    else printf("\nCreated Socket \n\n");
    bzero((char *) &serv_addr, sizeof(serv_addr));
    
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = htons(portid);
    
    
    //socket binding
    if (bind(sockfd, (struct sockaddr *) &serv_addr,
             sizeof(serv_addr)) < 0)
        error("ERROR on binding");
    else printf("Binding \n\n");
    
    
    
    // socket listening
    listen(sockfd,5);
    if (newsockfd < 0)
        error("ERROR on accept");
    else printf("Listening \n\n");
    clilen = sizeof(cli_addr);
    int notdone =1;
    
    
    //adding it to keep server running
    
    while (notdone) {
        
        
    //accept connections
        newsockfd = accept(sockfd,
                           (struct sockaddr *) &cli_addr,
                           &clilen);
        if (newsockfd < 0)
            error("ERROR on accept");
        else printf(" Accepting Connections \n\n");
        bzero(buffer,4096);
        n = read(newsockfd,buffer,4096);
        if (n < 0) error("ERROR reading from socket");
        
        printf("Here is the message: %s\n\n",buffer);
        
        if (n < 0) error("ERROR writing to socket");
        //char result[20] = system(buffer); // should I use execl(),pipe(),fork() etc ??instead  Ask
        
       
        
        
        //handling status
        
        
        if(strcmp(buffer,"Status")== 0){
            
//            result_code = pthread_create( &internal_threads[1], NULL, status,NULL );
//            assert( !result_code );
//            //
//            
//            result_code = pthread_join( internal_threads[1], NULL );
//            assert( !result_code );
            
            n = write(newsockfd,test_status,sizeof(test_status));
            if (n < 0) error("ERROR writing to socket");
           
            
            close(newsockfd);
        
        }
        else if (strcmp(buffer,"Result")== 0) {
            n = write(newsockfd,result,sizeof(result)-1);
             if (n < 0) error("ERROR writing to socket");
            close(newsockfd);
        }
   
        
            // execute the user command
        else {
            strcpy(test_status,"IN PROGRESS");
            strcpy(execution_command,buffer);
         strcpy(ack,"TEST CASE Recieved");
         n = write(newsockfd,ack,sizeof(ack));
            
            
            result_code = pthread_create( &internal_threads[0], NULL, test_execution, NULL);
            assert( !result_code );
        
        
       // else n = write(newsockfd,"Test Details recieved ..",22);
        if (n < 0) error("ERROR writing to socket");
        close(newsockfd);
        }
        
        
    }
    
    
    
    
    
    close(sockfd);
    
    return NULL;
}









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
    
    
    // create all threads one by one
    // for( index = 0; index < NUM_THREADS; ++index )
    
    
    // printf("In main: creating thread %d\n", 0);
    
    result_code = pthread_create( &threads[0], NULL, tcp_connection,&thread_args );
    assert( !result_code );
    
    
    

    
    
    // wait for each thread to complete
    // block until thread '0' completes
    result_code = pthread_join( threads[0], NULL );
    assert( !result_code );
    
    printf( "In main: All threads completed successfully\n" );
    exit( EXIT_SUCCESS );
}
