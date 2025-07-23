// Copyright 2019 Proyectos y Sistemas de Mantenimiento SL (eProsima).
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <utils/connection_logging.h>
#include <cstring>
#include <cstdlib>

extern "C" {

// Function to check if connection logging is enabled
// Use environment variable for reliable cross-process communication
bool is_connection_logging_enabled()
{
    const char* env_value = std::getenv("FASTDDS_CONNECTION_LOGGING");
    return (env_value != nullptr && strcmp(env_value, "1") == 0);
}

// Function to set connection logging state (called by server tool)
void set_connection_logging_enabled(bool enabled)
{
    if (enabled) {
        setenv("FASTDDS_CONNECTION_LOGGING", "1", 1);
    } else {
        unsetenv("FASTDDS_CONNECTION_LOGGING");
    }
}

// Function to check if a log category is connection-related
bool is_connection_log_category(const char* category)
{
    // Quick filter: check first character for performance
    if (category[0] != 'R') return false;
    
    // Check if it's exactly "RTPS_PDP_LISTENER"
    return strcmp(category, "RTPS_PDP_LISTENER") == 0;
}

}