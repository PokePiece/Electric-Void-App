#include "VoidBrain.h"
#include <iostream>
#include <string>

#ifdef USE_CURL
#include <curl/curl.h>
#include "json.hpp"
using json = nlohmann::json;

std::string callVoidAGI(const std::string& message) {
    CURL* curl = curl_easy_init();
    if (!curl) return "Error initializing CURL";

    std::string readBuffer;
    struct curl_slist* headers = nullptr;
    headers = curl_slist_append(headers, "Content-Type: application/json");

    json payload;
    payload["message"] = message;

    curl_easy_setopt(curl, CURLOPT_URL, "http://localhost:5000/chat");
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, payload.dump().c_str());

    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION,
        +[](char* ptr, size_t size, size_t nmemb, std::string* data) {
            data->append(ptr, size * nmemb);
            return size * nmemb;
        });
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);

    CURLcode res = curl_easy_perform(curl);
    curl_easy_cleanup(curl);

    if (res != CURLE_OK)
        return "Error in request";

    auto response = json::parse(readBuffer);
    std::string result = response["response"];
    std::cout << "Related Memory: \n";
    for (const auto& mem : response["memory"]) {
        std::cout << "- " << mem << std::endl;
    }

    return result;
}
#else
std::string callVoidAGI(const std::string& message) {
    (void)message;
    return "Curl support disabled";
}
#endif
