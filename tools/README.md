# Fast-DDS Tools

This directory contains tools and utilities for Fast-DDS, including Discovery Server, CLI tools, and configuration examples.

## 🚨 Quick Setup

**Prerequisites**: This assumes Fast-DDS is built in a ROS2 workspace structure:
```
$HOME/ros2_ws/
├── src/Fast-DDS/       # This repository
├── build/fastrtps/     # Build artifacts  
└── install/fastrtps/   # Installed binaries and tools
```

For logging functionality, build with Info logs enabled:

```bash
cd $HOME/ros2_ws
colcon build --packages-select fastrtps --cmake-args -DFASTDDS_ENFORCE_LOG_INFO=ON -DCMAKE_BUILD_TYPE=Debug
```

## 🛠️ Available Tools

### Discovery Server Options

**🐍 fastdds discovery** (Recommended)
- Python wrapper around the C++ binary
- Unified interface across tools  
- Installed in PATH: `$HOME/ros2_ws/install/fastrtps/bin/fastdds`
- Better integration with fastdds ecosystem

**⚙️ fast-discovery-server** (Direct Binary - Also Available)
- C++ binary with enhanced connection logging features
- **Also installed in PATH**: `$HOME/ros2_ws/install/fastrtps/bin/fast-discovery-server`
- Symlink to: `fast-discovery-serverd-1.0.1`
- Contains additional `--log-level` and `-c, --log-connections` options
- Direct access to C++ implementation

**Key Differences:**
- Both support the same core Discovery Server functionality
- Both support XML configuration files  
- Both are available in PATH and equally accessible
- The Python wrapper (`fastdds discovery`) simply forwards commands to the C++ binary
- **Enhanced logging features** (e.g., `--log-level`, `-c`) are available in both
- **Choice is mainly stylistic**: `fastdds discovery` for ecosystem consistency vs `fast-discovery-server` for directness

### CLI Tools

**🐍 fastdds** (Unified Python CLI - Recommended)
- **Type**: Shell script wrapper that calls Python scripts
- **Location**: `$HOME/ros2_ws/install/fastrtps/bin/fastdds`
- **Purpose**: Provides a unified, user-friendly interface for multiple Fast-DDS tools
- **Subcommands**:
  - `fastdds discovery` - Discovery Server management (wrapper for C++ binary)
  - `fastdds shm clean` - Clean zombie shared memory segments/ports
  - `fastdds xml validate` - Validate XML configuration files against XSD schemas

**Why Python CLI exists:**
1. **Unified Interface**: Single entry point for multiple tools
2. **Cross-platform Compatibility**: Handles path resolution and OS differences
3. **Enhanced Functionality**: Adds features like XML validation and SHM cleanup
4. **User Experience**: Provides consistent help, error handling, and output formatting
5. **Maintenance Tasks**: Automates common development/deployment operations

**🛠️ Individual Binaries** (Direct Access)
- **fast-discovery-server**: Direct C++ Discovery Server binary
- **ros-discovery**: ROS2-specific discovery utilities

## 📁 Directory Structure

```
tools/
├── README.md                    # This overview document
├── docs/                        # Detailed documentation
│   ├── connection-logging.md                        # Comprehensive logging guide
│   ├── discovery-server-comprehensive-analysis.md   # Discovery Server comprehensive analysis (English)
│   ├── discovery-server-comprehensive-analysis.ja.md # Discovery Server comprehensive analysis (Japanese)
│   ├── testing.md                                   # Testing procedures and commands  
│   └── xml-configurations.md                        # XML configuration file reference
├── examples/                    # Configuration examples
│   ├── fastdds_server_*.xml    # Server configuration files
│   └── fastdds_client_*.xml    # Client configuration files
├── fastdds/                     # Python CLI implementation
├── fds/                         # C++ Discovery Server source
└── CMakeLists.txt              # Build configuration
```

## 📚 Documentation

For detailed information, see:

- **[Connection Logging Guide](docs/connection-logging.md)** - Complete logging setup, configuration, testing, and troubleshooting
- **[Discovery Server Comprehensive Analysis](docs/discovery-server-comprehensive-analysis.md)** - Complete analysis of Discovery Server operation mechanisms, connection sequences, fallback conditions, and monitoring features (English)
- **[Discovery Server 包括的分析](docs/discovery-server-comprehensive-analysis.ja.md)** - Discovery Server の動作メカニズム、接続シーケンス、フォールバック条件、監視機能の包括的分析 (日本語)
- **[XML Configuration Guide](docs/xml-configurations.md)** - XML configuration files and usage examples

## 🚀 Quick Start

### Basic Discovery Server
```bash
# Method 1: Using Python wrapper (ecosystem consistency)
fastdds discovery -i 0
fastdds discovery -i 0 --log-level Info -c

# Method 2: Direct binary (more direct)
fast-discovery-server -i 0
fast-discovery-server -i 0 --log-level Info -c

# Both methods are equivalent and equally accessible
```

### With XML Configuration
```bash
# Python wrapper method
fastdds discovery -i 0 -x tools/examples/fastdds_server_monitor.xml

# Direct binary method
fast-discovery-server -i 0 -x tools/examples/fastdds_server_monitor.xml
```

### Client Connection
```bash
# Set Discovery Server for ROS2 nodes  
export ROS_DISCOVERY_SERVER=127.0.0.1:11811
ros2 run demo_nodes_cpp listener
```

## 🔧 Configuration Files

Pre-configured XML files are available in `tools/examples/`:

- `fastdds_server_monitor.xml` - Connection monitoring
- `fastdds_server_basic.xml` - Basic discovery logging
- `fastdds_server_verbose.xml` - Detailed debugging
- `fastdds_client_basic.xml` - Client configuration

## 🆘 Support

For detailed configuration, troubleshooting, and advanced usage, refer to the documentation in the `docs/` directory. Each guide provides comprehensive information for specific use cases.