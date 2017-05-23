#include <stdio.h>
#include <curl/curl.h>

int main(int argc, char** argv){

	if(argc != 3){
		printf("Usage: ./Login.c <IP> <Port>");
		return;
	}

	char* ip = argv[1];
	int port = atoi(argv[2]);

	if(connect(ip, port) < 0){
		return 2;
	}
	else{

		if(login() < 0){
			return 1;
		}
		else{
			return 0;
		}
			
	}

}


int connect(char* ip, int port){


	return -1;
}

int login(){


	return 0;
}

