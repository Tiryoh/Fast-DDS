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

#ifndef UTILS_CONNECTION_LOGGING_H_
#define UTILS_CONNECTION_LOGGING_H_

#include <cstdint>

#ifdef __cplusplus
extern "C" {
#endif

// Function to check if connection logging is enabled
__attribute__((visibility("default"))) bool is_connection_logging_enabled();

// Function to set connection logging state (called by server tool)
__attribute__((visibility("default"))) void set_connection_logging_enabled(bool enabled);

// Function to check if a log category is connection-related
__attribute__((visibility("default"))) bool is_connection_log_category(const char* category);

// Function to check if a locator is TCP transport (any port)
__attribute__((visibility("default"))) bool is_tcp_locator(int32_t locator_kind);

// Function to check if communication is TCP Discovery Server (supports any port)
__attribute__((visibility("default"))) bool is_tcp_discovery_server_communication(int32_t locator_kind, uint16_t port);

#ifdef __cplusplus
}
#endif

#endif // UTILS_CONNECTION_LOGGING_H_