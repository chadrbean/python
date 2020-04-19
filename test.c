#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <string.h>




int main( int argc, char *argv[] )
{
getpid( ) ; // a system call to show that we’ve entered this code
if ( argc < 2 )
{
printf( “hang (user|system)” ) ;
return 1 ;
}

if ( !strcmp( argv[1], “user” ) )
{
while ( 1 ) ;
}
else if ( !strcmp( argv[1], “system” ) )
{
sleep( 5000 ) ;
}
return 0 ;
}
