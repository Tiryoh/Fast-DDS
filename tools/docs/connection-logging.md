# Fast-DDS Connection Logging Guide

This document explains how to display logs for node discovery and other events in Fast-DDS.

## 🚨 **Essential Prerequisites (Most Important)**

**To enable Info logs in Fast-DDS 2.14.4, configuration according to CMAKE_BUILD_TYPE is required:**

### For Debug Build (Easy)
```bash
# ✅ FASTDDS_ENFORCE_LOG_INFO is enabled by default in Debug builds
colcon build --packages-select fastrtps --cmake-args -DCMAKE_BUILD_TYPE=Debug
```

### For Release Build (LOG_NO_INFO setting required)
```bash
# 🔴 Release builds have LOG_NO_INFO=ON by default, so explicit configuration is needed
colcon build --packages-select fastrtps --cmake-args -DFASTDDS_ENFORCE_LOG_INFO=ON -DLOG_NO_INFO=OFF -DCMAKE_BUILD_TYPE=Release
```

**⚠️ Important**: 
- **Debug Build**: `LOG_NO_INFO=OFF` by default → `FASTDDS_ENFORCE_LOG_INFO` is effective
- **Release Build**: `LOG_NO_INFO=ON` by default → `FASTDDS_ENFORCE_LOG_INFO` is ignored

## 📋 Table of Contents

1. [Log Overview](#log-overview)
2. [Node Discovery Logs](#node-discovery-logs)
3. [Discovery Server Extended Connection Logging Feature](#discovery-server-extended-connection-logging-feature)
4. [Log Configuration Methods](#log-configuration-methods)
5. [Practical Configuration Examples](#practical-configuration-examples)
6. [Testing Procedures](#testing-procedures)
7. [Troubleshooting](#troubleshooting)

## 📝 Log Overview

Fast-DDS uses its own logging system with the following characteristics:

### Log Levels
- **Error**: Highest priority, always output
- **Warning**: Medium priority, dynamically controllable
- **Info**: Lowest priority, for debugging (disabled by default)

### Log Categories (Node Discovery Related)
- `RTPS_PDP`: Participant Discovery Protocol
- `RTPS_PDP_DISCOVERY`: New Participant discovery
- `RTPS_PDP_LISTENER`: Participant registration in Discovery Server
- `RTPS_PDP_SERVER`: Discovery Server related

## 🔍 Node Discovery Logs

### Key Log Messages

#### 1. SPDP Message Reception
```
[INFO] [RTPS_PDP]: SPDP Message received from: <GUID>
```

#### 2. New Participant Discovery
```
[INFO] [RTPS_PDP_DISCOVERY]: New participant <GUID> at MTTLoc: <locators> DefLoc:<locators>
```

#### 3. Participant Registration (When using Discovery Server)
```
[INFO] [RTPS_PDP_LISTENER]: Registering a new participant: <GUID>
```

#### 4. Participant Update
```
[INFO] [RTPS_PDP_DISCOVERY]: Update participant <GUID>
```

## 🚀 Discovery Server Extended Connection Logging Feature

**Feature to selectively log node connections and disconnections in Fast-DDS 2.14.4 Discovery Server**

This feature allows you to view only important connection and disconnection information even at Warning log level.

### New Feature Overview

#### Added Command Line Arguments

##### `--log-level <level>`
Sets the log level.

```bash
fast-discovery-server -i 0 --log-level Info
```

**Supported levels**: Error, Warning, Info

##### `-c, --log-connections`  
Enables connection logging. Connection and disconnection logs are forcibly displayed even at Warning level.

```bash
fast-discovery-server -i 0 --log-level Warning -c
```

### Extended Log Messages

#### Detailed Connection Logs
```
[INFO] [RTPS_PDP_LISTENER]: PARTICIPANT CONNECTED - GUID: 01.02.03.04|0.0.1.c1 | Unicast Locators: UDPv4:[192.168.1.100]:7412 | Type: CLIENT
```

**Included information:**
- **GUID**: Participant unique ID
- **Unicast Locators**: Communication endpoint information
- **Type**: CLIENT/SERVER/OTHER

#### Detailed Disconnection Logs  
```
[INFO] [RTPS_PDP_LISTENER]: PARTICIPANT DISCONNECTED - GUID: 01.02.03.04|0.0.1.c1 | Reason: 2
```

**Included information:**  
- **GUID**: Participant unique ID
- **Reason**: Disconnection reason (numeric)
  - 1: DISCOVERED_PARTICIPANT
  - 2: DROPPED_PARTICIPANT  
  - 3: REMOVED_PARTICIPANT

### Usage Methods

#### Method 1: Display Connection Logs Only (Recommended)
```bash
# Warning level + forced connection log display
fast-discovery-server -i 0 --log-level Warning -c
```

#### Method 2: Display All Logs (Traditional Method)
```bash
# Display all logs at Info level
fast-discovery-server -i 0 --log-level Info
```

#### Method 3: XML File Configuration (Recommended)

Use predefined XML configuration files:
```bash
# Configuration for connection monitoring
fast-discovery-server -i 0 -x tools/examples/fastdds_server_monitor.xml

# Basic Discovery Server configuration
fast-discovery-server -i 0 -x tools/examples/fastdds_server_basic.xml

# Detailed debugging configuration
fast-discovery-server -i 0 -x tools/examples/fastdds_server_verbose.xml
```

**📄 For details on available XML configuration files, please refer to the [XML Configuration Guide](xml-configurations.md).**

### Practical Examples

#### For Connection Monitoring (Recommended)
```bash
# Start Discovery Server (connection logs only)
fast-discovery-server -i 0 --log-level Warning -c

# Start client in another terminal
export ROS_DISCOVERY_SERVER="127.0.0.1:11811"
ros2 run demo_nodes_cpp listener
```

#### For Debugging (All Logs)
```bash
# Start Discovery Server (detailed logs)
fast-discovery-server -i 0 --log-level Info

# Start client in another terminal
export ROS_DISCOVERY_SERVER="127.0.0.1:11811"
ros2 run demo_nodes_cpp listener
```

#### Log File Output
```bash
# Output connection logs to file
fast-discovery-server -i 0 --log-level Warning -c 2>&1 | tee discovery.log
```

### Technical Details

#### Modified Files
- `tools/fds/server.h`: `--log-connections` option definition
- `tools/fds/server.cpp`: Option processing, environment variable configuration
- `src/cpp/utils/connection_logging.h/.cpp`: State management functions
- `include/fastdds/dds/log/Log.hpp`: Log macro extensions

#### APIs Used
- `is_connection_logging_enabled()`: Check connection logging enabled state
- `is_connection_log_category()`: Determine connection log category
- `EPROSIMA_LOG_INFO()`: Log output macro (extended)

### Important Notes

1. **Selective Output**: Connection logs are displayed at Warning level only when the `-c` option is specified
2. **Filtering**: Only connection-related logs in the `RTPS_PDP_LISTENER` category are targeted
3. **Performance**: There is a minor performance impact due to log judgment processing
4. **Compatibility**: All existing options and log level settings continue to work

This implementation enables real-time monitoring of node connection status in Discovery Server.

## ⚙️ Log Configuration Methods

⚠️ **Important**: The `FASTDDS_LOG_LEVEL` environment variable is **not implemented in any version**.

🚨 **Features not configurable via XML in Fast-DDS 2.14.4:**
- `<logging_level>` - Set via command line arguments or API  
- `<category_filter>` - Configurable only via API
- `<report_filenames>` - Configurable only via API
- `<report_functions>` - Configurable only via API

Use XML files or in-program configuration instead.

### 🔴 Prerequisites (Required)

**Before using the configuration methods below, make sure to complete the build-time configuration in the "Essential Prerequisites" section above.**

### Method 1: XML File Configuration (Recommended)

#### ⚡ Important: Configuration Priority

**XML file settings take precedence over command line arguments:**

```bash
# Using both command line arguments and XML file
fastdds discovery -i 0 --log-level Warning -x tools/examples/fastdds_server_monitor.xml
```

**Processing order:**
1. Command line arguments (`--log-level`) are processed first
2. XML file is loaded later, and additional consumer settings are applied
3. **XML file configures output destinations, not log levels**

#### Using Predefined XML Files (Easiest)

Use predefined XML files in tools/examples/:

```bash
# Specify via environment variable
export FASTDDS_DEFAULT_PROFILES_FILE="tools/examples/fastdds_server_monitor.xml"

# Or specify at runtime
fast-discovery-server -i 0 -x tools/examples/fastdds_server_monitor.xml
```

**📄 For details on available XML configuration files, please refer to the [XML Configuration Guide](xml-configurations.md).**

#### Creating Custom XML Files (Advanced Configuration)

Complete XML profile example for custom configuration needs:

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<profiles xmlns="http://www.eprosima.com/XMLSchemas/fastRTPS_Profiles">
    <log>
        <use_default>false</use_default>
        <consumer>
            <class>StdoutErrConsumer</class>
            <property>
                <name>stderr_threshold</name>
                <value>Log::Kind::Info</value>
            </property>
        </consumer>
        <!-- Note: The following features cannot be configured via XML in Fast-DDS 2.14.4 -->
        <!-- Log level, category filters, filename/function name display must be -->
        <!-- configured via API usage in programs or command line arguments -->
    </log>
</profiles>
```

### Method 2: In-Program Configuration

```cpp
#include <fastdds/dds/log/Log.hpp>
#include <regex>

// Set log level
eprosima::fastdds::dds::Log::SetVerbosity(eprosima::fastdds::dds::Log::Kind::Info);

// Display only specific categories (optional)
eprosima::fastdds::dds::Log::SetCategoryFilter(std::regex("RTPS_PDP.*"));

// Enable filename display (optional)
eprosima::fastdds::dds::Log::ReportFilenames(true);

// Enable function name display (optional)
eprosima::fastdds::dds::Log::ReportFunctions(true);
```

### Method 3: CMake Build-time Configuration (Same as "Essential Prerequisites" above)

**⚠️ This configuration should already be completed in the "Essential Prerequisites" section.**

```bash
# For Debug build (recommended)
colcon build --packages-select fastrtps --cmake-args -DCMAKE_BUILD_TYPE=Debug

# For Release build
colcon build --packages-select fastrtps --cmake-args -DFASTDDS_ENFORCE_LOG_INFO=ON -DLOG_NO_INFO=OFF -DCMAKE_BUILD_TYPE=Release

# Or for standalone build
cmake .. -DFASTDDS_ENFORCE_LOG_INFO=ON -DLOG_NO_INFO=OFF -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
```

**Build-time log macro control:**

```bash
# Completely disable specific log levels
cmake .. -DLOG_NO_INFO=ON      # Disable Info logs
cmake .. -DLOG_NO_WARNING=ON   # Disable Warning logs
cmake .. -DLOG_NO_ERROR=ON     # Disable Error logs
```

### Method 4: File Output Configuration

```xml
<log>
    <use_default>false</use_default>
    
    <!-- File output -->
    <consumer>
        <class>FileConsumer</class>
        <property>
            <name>filename</name>
            <value>fastdds_discovery.log</value>
        </property>
        <property>
            <name>append</name>
            <value>true</value>
        </property>
    </consumer>
    
    <!-- Note: Log level configuration is done via command line arguments -->
    <!-- fast-discovery-server -i 0 --log-level Info -x this_file.xml -->
</log>
```

## 🔧 Practical Configuration Examples

**✅ Note**: Since `FASTDDS_ENFORCE_LOG_INFO` is ON by default, the following configuration examples can be used with normal builds.

### 1. Using Predefined XML Files

The easiest and most practical method is to use predefined XML files:

```bash
# Optimal for connection monitoring
fastdds discovery -i 0 -x tools/examples/fastdds_server_monitor.xml

# Basic Discovery Server
fastdds discovery -i 0 -x tools/examples/fastdds_server_basic.xml

# For detailed debugging
fastdds discovery -i 0 -x tools/examples/fastdds_server_verbose.xml
```

**📄 For details and comparisons of each XML file, please refer to the [XML Configuration Guide](xml-configurations.md).**

### 3. Dynamic In-Program Configuration

```cpp
// Change log level during runtime
eprosima::fastdds::dds::Log::SetVerbosity(eprosima::fastdds::dds::Log::Kind::Info);

// Display only Discovery-related logs
eprosima::fastdds::dds::Log::SetCategoryFilter(std::regex("RTPS_PDP.*"));

// Reset filter
eprosima::fastdds::dds::Log::UnsetCategoryFilter();

// Flush logs
eprosima::fastdds::dds::Log::Flush();
```

### 4. File Output + Console Output

```xml
<log>
    <use_default>false</use_default>
    
    <!-- Console output -->
    <consumer>
        <class>StdoutErrConsumer</class>
        <property>
            <name>stderr_threshold</name>
            <value>Log::Kind::Info</value>
        </property>
    </consumer>
    
    <!-- File output -->
    <consumer>
        <class>FileConsumer</class>
        <property>
            <name>filename</name>
            <value>/tmp/fastdds_discovery.log</value>
        </property>
        <property>
            <name>append</name>
            <value>true</value>
        </property>
    </consumer>
    
    <!-- Note: Log level and category filters require in-program configuration -->
</log>
```

## 🧪 Testing Procedures

You can test the Discovery Server connection logging functionality with the following procedures.

### Basic Function Verification

#### 1. Verify Command Line Options
```bash
# Using Python wrapper
fastdds discovery --help

# Using binary directly  
fast-discovery-server --help
```

#### 2. Test Log Level Settings
```bash
# Test startup at Info level
fastdds discovery -i 0 --log-level Info

# Test startup at Warning level  
fastdds discovery -i 0 --log-level Warning

# Test startup at Error level (default)
fastdds discovery -i 0 --log-level Error
```

#### 3. Verify Error Handling for Invalid Options
```bash
# Invalid log level
fastdds discovery -i 0 --log-level InvalidLevel

# Verify that appropriate error messages and help are displayed
```

### Actual Connection Log Testing

#### Terminal 1: Start Discovery Server
```bash
# Start server with connection logging enabled
fastdds discovery -i 0 --log-level Info -c
```

#### Terminal 2: Connect ROS2 Client
```bash
# Configure to use Discovery Server
export ROS_DISCOVERY_SERVER=127.0.0.1:11811

# Start test node
ros2 run demo_nodes_cpp listener
```

#### Terminal 3: Connect Additional Client
```bash
export ROS_DISCOVERY_SERVER=127.0.0.1:11811
ros2 run demo_nodes_cpp talker
```

### Expected Output

The following logs will be displayed in Terminal 1's Discovery Server:

**On Connection:**
```
[INFO] [RTPS_PDP_LISTENER]: PARTICIPANT CONNECTED - GUID: 01.02.03.04|0.0.1.c1 | Unicast Locators: UDPv4:[192.168.1.100]:7412 | Type: CLIENT
[INFO] [RTPS_PDP_LISTENER]: PARTICIPANT CONNECTED - GUID: 01.02.03.04|0.0.2.c1 | Unicast Locators: UDPv4:[192.168.1.100]:7413 | Type: CLIENT
```

**On Disconnection (when node stops):**
```
[INFO] [RTPS_PDP_LISTENER]: PARTICIPANT DISCONNECTED - GUID: 01.02.03.04|0.0.1.c1 | Reason: 2
```

### Test XML File Configuration

```bash
# Test with predefined XML configuration
fastdds discovery -i 0 -x tools/examples/fastdds_server_monitor.xml

# Test with custom XML configuration (e.g., minimal configuration)
fastdds discovery -i 0 -x tools/examples/fastdds_server_minimal.xml
```

### Simple Diagnostic Procedures

If logs are not displayed:

1. **Check environment variables**:
   ```bash
   echo $ROS_DISCOVERY_SERVER
   # Should output 127.0.0.1:11811
   ```

2. **Check port usage**:
   ```bash
   netstat -an | grep 11811
   ```

3. **Test with different port**:
   ```bash
   # Test with different port
   fastdds discovery -i 1 -l 127.0.0.1 -p 11812 --log-level Info
   ```

## 🚨 Troubleshooting

### When Logs Are Not Displayed

1. **✅ Top Priority Check: Verify Build-time Configuration**
   ```bash
   # Check LOG_NO_INFO and FASTDDS_ENFORCE_LOG_INFO settings
   grep -E "(LOG_NO_INFO|FASTDDS_ENFORCE_LOG_INFO)" $HOME/ros2_ws/build/fastrtps/CMakeCache.txt
   
   # For Release build, both settings are required
   colcon build --packages-select fastrtps --cmake-args -DFASTDDS_ENFORCE_LOG_INFO=ON -DLOG_NO_INFO=OFF -DCMAKE_BUILD_TYPE=Release
   
   # For Debug build, it's simple
   colcon build --packages-select fastrtps --cmake-args -DCMAKE_BUILD_TYPE=Debug
   ```

2. **Check XML Files**
   ```bash
   # Check if XML file is loaded correctly
   echo $FASTDDS_DEFAULT_PROFILES_FILE
   ls -la $FASTDDS_DEFAULT_PROFILES_FILE
   ```

3. **Verify XML File Syntax**
   ```bash
   # Check XML file syntax
   xmllint --noout your_log_config.xml
   
   # Check syntax of extension XML files
   xmllint --noout tools/examples/fastdds_server_monitor.xml
   ```

4. **Check Category Filters**
   ```cpp
   // Check filter status in program
   if (eprosima::fastdds::dds::Log::HasCategoryFilter()) {
       std::cout << "Category filter is active" << std::endl;
       std::regex filter = eprosima::fastdds::dds::Log::GetCategoryFilter();
   }
   ```

### Common Problems and Solutions

| Problem | Cause | Solution |
|---------|-------|----------|
| **🔴 Info logs not displayed** | **LOG_NO_INFO=ON in Release build** | **Add `-DLOG_NO_INFO=OFF` and rebuild** |
| `--log-level Info` not working | Insufficient build-time configuration | Rebuild with `FASTDDS_ENFORCE_LOG_INFO=ON`, combine with XML file |
| Different behavior between XML and command line | Log level cannot be set via XML in 2.14.4 | Set log level via command line, consumer configuration via XML |
| Environment variable `FASTDDS_LOG_LEVEL` not working | Not implemented | Use XML or in-program configuration |
| `fast-discovery-server --log-level` not recognized | Extension feature not built | Use binary that includes the above extensions |
| Extended connection logs not displayed | Log level or category filter issue | Check `Info` level, `RTPS_PDP_LISTENER` category |
| Extension XML not loaded | Incorrect XML file path | Use absolute path and verify XML file exists |
| Too many logs | All categories are displayed | Set category filter |
| XML file not loaded | Incorrect path | Use absolute path |
| Log file not created | Directory does not exist | Create directory beforehand |

### Debug Configuration

**Maximum log output configuration:**
```xml
<log>
    <use_default>false</use_default>
    <consumer>
        <class>StdoutErrConsumer</class>
        <property>
            <name>stderr_threshold</name>
            <value>Log::Kind::Info</value>
        </property>
    </consumer>
    <!-- Note: The following must be configured in-program in Fast-DDS 2.14.4 -->
    <!-- Log level: --log-level Info -->
    <!-- Filename display: eprosima::fastdds::dds::Log::ReportFilenames(true) -->
    <!-- Function name display: eprosima::fastdds::dds::Log::ReportFunctions(true) -->
</log>
```

## 📚 Reference Information

### Key Log Categories List

| Category | Description |
|----------|-------------|
| `RTPS_PDP` | Participant Discovery Protocol basics |
| `RTPS_PDP_DISCOVERY` | Participant discovery and updates |
| `RTPS_PDP_LISTENER` | **Registration in Discovery Server (includes extended connection logs)** |
| `RTPS_PDP_SERVER` | Discovery Server specific |
| `RTPS_EDP` | Endpoint Discovery Protocol |
| `RTPS_PARTICIPANT` | Participant operations |
| `CLI` | CLI tool related |
| `RTPS_DOMAIN` | Domain operations |
| `SECURITY` | Security related |

### Available Log Consumers

| Class | Description |
|-------|-------------|
| `StdoutConsumer` | Output to standard output |
| `FileConsumer` | Output to file |

### Log Level and Macro Correspondence

| Level | XML Specification | Macro | Default State |
|-------|-------------------|-------|---------------|
| Error | `Error` | `EPROSIMA_LOG_ERROR` | Always enabled |
| Warning | `Warning` | `EPROSIMA_LOG_WARNING` | Enabled |
| Info | `Info` | `EPROSIMA_LOG_INFO` | Disabled in release builds |

### How to Check Fast-DDS Version

```bash
# Check version
fastdds discovery -v

# Or
fast-discovery-server -v
```

---

**Important Notes**: 
- **⚠️ Release builds have LOG_NO_INFO=ON by default**, requiring explicit `-DLOG_NO_INFO=OFF`
- **✅ Debug builds have LOG_NO_INFO=OFF by default**, no additional configuration needed
- **The `FASTDDS_LOG_LEVEL` environment variable is not implemented** (in both Fast-DDS 2.x and 3.x)
- **XML file configuration** or **in-program API configuration** work reliably
- Information found online may contain errors. Always verify with actual source code
- This document is based on the Fast-DDS 2.14.4 implementation

## 📁 Related Documents

- [XML Configuration Guide](xml-configurations.md) - Details on XML configuration files