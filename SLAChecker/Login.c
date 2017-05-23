#include <stdio.h>
#include <curl/curl.h>
#include <stdlib.h>
#include <string.h>

struct recv_data{
	char * data;
	size_t size;
};

static size_t WriteMemoryCallback(void *contents, size_t size, size_t nmemb, void *userp)
{
  size_t realsize = size * nmemb;
  struct recv_data *data = (struct recv_data *)userp;

  data->data = realloc(data->data, data->size + realsize + 1);
  
  if(data->data == NULL) {
    printf("not enough memory (realloc returned NULL)\n");
    return 0;
  }
  
  memcpy(&(data->data[data->size]), contents, realsize);
  data->size += realsize;
  data->data[data->size] = 0;

  return realsize;
}

int main(int argc, char** argv){

	if(argc != 3){
		printf("Usage: ./Login.c <IP> <Port>");
		return;
	}

	char* ip = argv[1];
	int port = atoi(argv[2]);

	if(connecturl(ip, port) < 0){
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


int connecturl(char* ip, int port){

	CURL *curl;

	CURLcode res;

	struct recv_data data;
	data.data = malloc(1);
	data.size = 0;

	curl = curl_easy_init();

	if(curl){

		curl_easy_setopt(curl, CURLOPT_URL, "http://www.example.com/");
		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);
		curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void*) &data);


		res = curl_easy_perform(curl);
		
		if(res != CURLE_OK) 
			fprintf(stderr, "curl,easy_perform() failed: %s\n", curl_easy_strerror(res));
		else{

			printf("%lu\n", data.size);

		}


		curl_easy_cleanup(curl);
	}

	return -1;
}

int login(){


	return 0;
}

