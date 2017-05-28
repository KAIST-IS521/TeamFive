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

int connecturl(char* ip, char* port, char* id, char* password){

	CURL *curl;

	CURLcode res;

	struct recv_data data;

	char temp[512];

	data.data = malloc(1);
	data.size = 0;

	curl = curl_easy_init();

	if(curl){

		char url[128];

		strcpy(url, ip);
		strcat(url, ":");
		strcat(url, port);
		strcat(url, "/bbs/login/");

		printf("target: %s", url);

		//curl_easy_setopt(curl, CURLOPT_URL, "127.0.0.1:12345/bbs/login/");
		curl_easy_setopt(curl, CURLOPT_URL, url);
		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);
		curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void*) &data);
		curl_easy_setopt(curl, CURLOPT_COOKIEFILE, "./coo.txt");
		//curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L);

		res = curl_easy_perform(curl);
		
		if(res != CURLE_OK){
				fprintf(stderr, "curl,easy_perform() failed: %s\n", curl_easy_strerror(res));
				return -1;
			}
		else{
			//printf("%s\n", data);

			struct curl_slist *cookies = NULL;
			
			res = curl_easy_getinfo(curl, CURLINFO_COOKIELIST, &cookies);

			char* ptr;

			if(!res && cookies){
			
			//printf("%s\n", cookies->data);

			ptr = strtok(cookies->data, "\t");
			ptr = strtok(NULL, "\t");
			ptr = strtok(NULL, "\t");
			ptr = strtok(NULL, "\t");
			ptr = strtok(NULL, "\t");
			ptr = strtok(NULL, "\t");
			ptr = strtok(NULL, "\t");


			//printf("%s\n", ptr);

			curl_easy_setopt(curl, CURLOPT_URL, "127.0.0.1:12345/bbs/login/");
			//strcat(temp, "username=bjgwak&password=bbbbbbbb&csrfmiddlewaretoken=");

			strcat(temp, "username=");
			strcat(temp, id);
			strcat(temp, "&password=");
			strcat(temp, password);
			strcat(temp, "&csrfmiddlewaretoken=");


			strcat(temp, ptr);

			curl_easy_setopt(curl, CURLOPT_POSTFIELDS, temp);
			curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);
			curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void*) &data);
			curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L);
		
			
		

			res = curl_easy_perform(curl);

			//printf("%s\n", data.data);

			}


			
			return 0;

		}


	}

}

int login(char* id, char* password){

	return 0;
}

int main(int argc, char** argv){

	if(argc != 3){
		printf("Usage: ./Login.c <IP> <Port>");
		return;
	}

	char* ip = argv[1];
	char* port = argv[2];

	char id[25];
	char password[25];

	FILE* fp = fopen("./account.csv", "r");

	char line[128];

	while(fgets(line, 128, fp)){

		char* temp = strtok(line, ",");

		strcpy(id, temp);

		temp = strtok(NULL, "");

		strcpy(password, temp);

		password[strlen(password)-1] = '\0';		

		int result = connecturl(ip, port, id, password);
		
		switch(result){

		case -1: printf("connection error: %s:%s\n", ip, port); return 2; 

		case 0: printf("%s/%s: Login success\n", id, password); return 0;

		case 1: printf("%s/%s: Login failure\n", id, password); return 1;

		}

	}




}

