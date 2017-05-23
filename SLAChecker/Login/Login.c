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

		//parse_csv(id,password)

		char* id;
		char* password;

		if(login(id, password) < 0){	//login(id, password)
			printf("Login error\n");
			return 1;
		}
		else{
			printf("Login successfully\n");
			return 0;
		}
			
	}

}

int connecturl(char* ip, int port){

	CURL *curl;

	CURLcode res;

	struct recv_data data;

	struct curl_slist *cookies;
	

	data.data = malloc(1);
	data.size = 0;

	curl = curl_easy_init();

	if(curl){

		curl_easy_setopt(curl, CURLOPT_URL, "127.0.0.1:12345/bbs/");
		//curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);
		//curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void*) &data);
		curl_easy_setopt(curl, CURLOPT_COOKIEFILE, "-");

		res = curl_easy_perform(curl);
		
		if(res != CURLE_OK) 
			{
				fprintf(stderr, "curl,easy_perform() failed: %s\n", curl_easy_strerror(res));

			
				return -1;
			}
		else{

			printf("Enter the bbs page successfully\n");

			res = curl_easy_getinfo(curl, CURLINFO_COOKIELIST, &cookies);

		/*curl_easy_setopt(curl, CURLOPT_URL, "127.0.0.1:12345/bbs/login/");
		curl_easy_setopt(curl, CURLOPT_POSTFIELDS, "username=bjgwak&password=bbbbbbbb&csrfmiddlewaretoken=CSRF_TOKEN");
		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);
		curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void*) &data);*/
		if(!res && cookies){
			while(cookies){
				printf("%s\n", cookies->data);
				}
		}

		//res = curl_easy_perform(curl);

//printf("%s\n", data.data);
			
			return -1;

		}


	}

}

int login(char* id, char* password){
	
	CURL *curl;

	CURLcode res;

	struct recv_data data;
	data.data = malloc(1);
	data.size = 0;

	curl = curl_easy_init();

	if(curl){

		curl_easy_setopt(curl, CURLOPT_URL, "127.0.0.1:12345/bbs/login/");
		curl_easy_setopt(curl, CURLOPT_POSTFIELDS, "username=bjgwak&password=bbbbbbbb");
		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);
		curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void*) &data);


		res = curl_easy_perform(curl);
		
		if(res != CURLE_OK) 
			{
				fprintf(stderr, "curl,easy_perform() failed: %s\n", curl_easy_strerror(res));

			
				return -1;
			}
		else{

			printf("%s\n", data.data);

			
			return 0;

		}


	}
}

