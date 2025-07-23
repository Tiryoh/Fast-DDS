# Fast-DDS XML Configuration Files (v2.14.4 Compatible Version)

**⚠️ Important: This document is based on Fast-DDS v2.14.4 implementation.**

This directory contains XML configuration files for Fast-DDS log output and Discovery Server setup.

## 🚨 Important Implementation Status Clarification

**❌ Features not implemented/not XML-supported in v2.14.4:**
- `<logging_level>` - Cannot be configured via XML (API only)
- `<category_filter>` - Cannot be configured via XML (API only)  
- `<report_functions>` - Cannot be configured via XML (API only)

**Confirmation through source code investigation** (`src/cpp/rtps/xmlparser/XMLParser.cpp:1796-2070`):
- XML parser only implements Consumer configuration
- No XML element processing code exists for log level or category filter

<details>
<summary>🚨 Legacy Documentation (Contains v3.x Features - Implementation Incomplete)</summary>

This section contains feature descriptions for future versions, but **they are not implemented in v2.14.4**.

## 📋 Available Configurations (For Future Versions)

### 🖥️ Server Configurations

**`fastdds_server_monitor.xml`**
- **Purpose**: Track participant connections/disconnections on server side
- **Features**: RTPS_PDP_LISTENER category filter, function names, connection tracking
- **Usage**: `fastdds discovery -i 0 -x tools/examples/fastdds_server_monitor.xml`

**`fastdds_server_basic.xml`**
- **Purpose**: Basic Discovery Server with connection logging
- **Features**: SERVER protocol, RTPS_PDP_LISTENER logging
- **Usage**: `fastdds discovery -i 0 -x tools/examples/fastdds_server_basic.xml`

**`fastdds_server_verbose.xml`**
- **Purpose**: Comprehensive logging for detailed debugging
- **Features**: All Info level categories, StdoutErrConsumer
- **Usage**: `fastdds discovery -i 0 -x tools/examples/fastdds_server_verbose.xml`

**`fastdds_server_minimal.xml`**
- **Purpose**: Minimal server setup with basic logging
- **Features**: Simple Info logging, minimal overhead
- **Usage**: `fastdds discovery -i 0 -x tools/examples/fastdds_server_minimal.xml`

### 👥 Client Configurations
**`fastdds_client_basic.xml`**
- **Purpose**: Client-side participant configuration
- **Features**: CLIENT protocol, connects to 127.0.0.1:11811, basic logging
- **Usage**: Set `FASTDDS_DEFAULT_PROFILES_FILE=tools/examples/fastdds_client_basic.xml` for applications

## 🔧 Customization (For Future Versions)

All files can be customized by modifying:
- `<logging_level>`: Error, Warning, Info
- `<category_filter>`: Regular expression patterns for log categories
- `<report_functions>`: true/false for function name display
- Network addresses and ports in participant configuration

## 📊 Configuration Comparison (For Future Versions)

| File | Log Scope | Performance | Use Case |
|----------|----------|----------------|------------|
| `fastdds_server_monitor.xml` | Connection events only | High | Production monitoring |
| `fastdds_server_basic.xml` | Discovery events | Medium | Development |
| `fastdds_server_verbose.xml` | All categories | Low | Detailed debugging |
| `fastdds_server_minimal.xml` | Basic Info | High | Lightweight setup |
| `fastdds_client_basic.xml` | Client side | Medium | Application testing |

</details>

## 📋 Actually Available XML Configurations in v2.14.4

### ✅ Implemented Features

#### Log Consumer Configuration
```xml
<log>
    <use_default>true</use_default>  <!-- ON/OFF for using default log -->
    <consumer>
        <class>StdoutErrConsumer</class>  <!-- or StdoutConsumer, FileConsumer -->
        <property>
            <name>stderr_threshold</name>
            <value>Log::Kind::Info</value>  <!-- Info/Warning/Error -->
        </property>
    </consumer>
</log>
```

#### Discovery Server Configuration
```xml
<participant profile_name="discovery_server_participant" is_default_profile="true">
    <domainId>0</domainId>
    <rtps>
        <builtin>
            <discovery_config>
                <discoveryProtocol>SERVER</discoveryProtocol>  <!-- SERVER/CLIENT/SIMPLE etc -->
                <discoveryServersList>
                    <RemoteServer prefix="44.53.00.5f.45.50.52.4f.53.49.4d.41">
                        <metatrafficUnicastLocatorList>
                            <locator>
                                <udpv4>
                                    <address>127.0.0.1</address>
                                    <port>11811</port>
                                </udpv4>
                            </locator>
                        </metatrafficUnicastLocatorList>
                    </RemoteServer>
                </discoveryServersList>
            </discovery_config>
        </builtin>
        <prefix>44.53.00.5f.45.50.52.4f.53.49.4d.41</prefix>
    </rtps>
</participant>
```

### ❌ Features Not Implemented in v2.14.4

The following features exist as APIs but cannot be configured via XML:

- **Log Level Setting**: `<logging_level>` - Set from program using `Log::SetVerbosity()`
- **Category Filter**: `<category_filter>` - Set from program using `Log::SetCategoryFilter()`
- **Function Name Display**: `<report_functions>` - Set from program using `Log::ReportFunctions()`

## 🚨 Prerequisites

**⚠️ Configuration according to build type is required:**

```bash
cd $HOME/ros2_ws

# For Debug build (recommended, easy)
colcon build --packages-select fastrtps --cmake-args -DCMAKE_BUILD_TYPE=Debug

# For Release build (LOG_NO_INFO specification required)
colcon build --packages-select fastrtps --cmake-args -DFASTDDS_ENFORCE_LOG_INFO=ON -DLOG_NO_INFO=OFF -DCMAKE_BUILD_TYPE=Release
```

**⚠️ Important**: 
- **Debug Build**: `LOG_NO_INFO=OFF` by default → Info logs are enabled
- **Release Build**: `LOG_NO_INFO=ON` by default → Explicitly `-DLOG_NO_INFO=OFF` is required

## 💡 Actual Usage Examples in v2.14.4

### Basic Discovery Server Startup
```bash
# Terminal 1: Start Discovery Server
fastdds discovery -i 0 -x tools/examples/fastdds_server_basic.xml

# Terminal 2: Start client
export FASTDDS_DEFAULT_PROFILES_FILE="tools/examples/fastdds_client_basic.xml"
your_application
```

### Using Extended Connection Logging Feature (see connection-logging.md)
```bash
# Display connection logs only (recommended)
fastdds discovery -i 0 --log-level Warning -c

# Display detailed logs
fastdds discovery -i 0 --log-level Info

# Combine with XML file
fastdds discovery -i 0 --log-level Info -x tools/examples/fastdds_server_monitor.xml
```

### Log Control from Program (Parts that cannot be configured via XML)
```cpp
// Log configuration within C++ code (not possible via XML)
#include <fastdds/log/Log.hpp>

// Set log level
eprosima::fastdds::dds::Log::SetVerbosity(eprosima::fastdds::dds::Log::Kind::Info);

// Set category filter
eprosima::fastdds::dds::Log::SetCategoryFilter(std::regex("RTPS_PDP_LISTENER"));

// Enable function name display
eprosima::fastdds::dds::Log::ReportFunctions(true);
```

## 📁 File Locations

All XML configuration files are located in:
```
tools/examples/
├── fastdds_server_monitor.xml    (Log consumer config + SERVER participant config)
├── fastdds_server_basic.xml      (Log consumer config + SERVER participant config)
├── fastdds_server_verbose.xml    (Log consumer config + SERVER participant config)
├── fastdds_server_minimal.xml    (Log consumer config + SERVER participant config)
└── fastdds_client_basic.xml      (Log consumer config + CLIENT participant config)
```

## 📚 Related Documentation

- [Connection Logging Guide](connection-logging.md) - Detailed log configuration, extended connection logging features, testing procedures, troubleshooting

## 📝 Implementation Status Summary

| Feature | XML Config | API Config | v2.14.4 Support |
|------|---------|---------|-------------|
| Log Consumer | ✅ | ✅ | Full support |
| Discovery Server Config | ✅ | ✅ | Full support |
| Log Level | ❌ | ✅ | API only |
| Category Filter | ❌ | ✅ | API only |
| Function Name Display | ❌ | ✅ | API only |

**Conclusion**: In v2.14.4, XML files are mainly limited to "log output destinations" and "Discovery Server connection settings". Advanced log control requires using the C++ API.
