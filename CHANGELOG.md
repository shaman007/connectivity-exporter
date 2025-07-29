# Changelog

## 2025-05-15 – `6132e35` by Andrey Bondarenko
- **License Update**
  - Added GNU General Public License v3 to the project as `LICENSE`.

- **Documentation**
  - No changes made to `README.md`. 

**Note:** The addition of the LICENSE file may affect the distribution and usage rights of the software.

## 2025-05-15 – `fff7fed` by Andrey Bondarenko
- **New Feature: Connectivity Checker**
  - Added `connectivity-exporter.py` for monitoring endpoint connectivity with Prometheus metrics.
  - Implements configurable endpoint checks with customizable intervals and expected HTTP status codes.

- **Configuration and Metrics**
  - Supports YAML configuration for defining endpoints.
  - Exposes metrics: `connectivity_status` and `connectivity_time_ms` for Prometheus.

- **Command-Line Interface**
  - CLI options for port, interval, and config file path, with environment variable support.

- **Error Handling**
  - Improved error handling for HTTP requests and configuration loading.

- **Threading**
  - Utilizes threading for continuous endpoint checks without blocking the main thread.

## 2025-05-15 – `934c30f` by Andrey Bondarenko
- **New Features**
  - Added `Dockerfile` for containerization of the connectivity exporter.
  - Introduced `deployment.yaml` for Kubernetes deployment, including ConfigMap and Service definitions.

- **Configuration**
  - New `config.yaml` with predefined endpoints for connectivity checks.
  - Updated `README.md` with usage instructions and sample configurations.

- **Code Changes**
  - Modified `connectivity-exporter.py` to change default port from 8443 to 9090.
  - Added `run` script to execute the exporter with the specified configuration.

- **Important Files**
  - `Dockerfile`, `deployment.yaml`, `config.yaml`, and `run` are newly created.
  
- **Breaking Changes**
  - Default port change from 8443 to 9090 may affect existing deployments.

## 2025-05-15 – `0a069f8` by Andrey Bondarenko
- **Documentation Update**
  - Added inspiration source link to README.md for clarity on project motivation.

## 2025-05-15 – `89cf5b7` by Andrey Bondarenko
- **Dockerfile Updates**
  - Added `RUN chmod +x /etc/run` to make the `run` script executable.
  - Ensured installation of `prometheus_client` and `pyyaml` without cache.

## 2025-05-15 – `600563d` by Andrey Bondarenko
- **Dockerfile Updates**
  - Added installation of `dumb-init` for better process management.
  - Included commands for updating, upgrading, and cleaning up APT packages.
  - Ensured removal of temporary files to reduce image size.

## 2025-05-15 – `fc1491d` by Andrey Bondarenko
- **Script Modification**: 
  - Removed Bash shebang and error handling from `run` script.
  
- **Execution Change**: 
  - Directly executes Python script `check.py` with specified config. 

- **File Structure**: 
  - No newline added at the end of the `run` file. 

**Breaking Change**: The script is no longer a Bash script and will not handle errors as before.

## 2025-05-15 – `fbfac53` by Andrey Bondarenko
- **Documentation Update**
  - Added image to `README.md` for visual enhancement.
  - Updated description to clarify usage of the connectivity-exporter.

## 2025-05-15 – `8561627` by Andrey Bondarenko
- **Documentation Update:**
  - Removed quotes from `job_name` in YAML configuration in `README.md`.
  - Adjusted formatting for `targets` in YAML configuration in `README.md`.

## 2025-05-15 – `7ec36dc` by Andrey Bondarenko
- **Documentation Update**
  - Added deployment image reference to `README.md`: `harbor.andreybondarenko.com/library/connectivity-exporter:latest`.
  - Corrected punctuation in deployment section of `README.md`.

## 2025-05-15 – `bade775` by Andrey Bondarenko
- **Documentation Updates**
  - Added note about Dockerfile and Kubernetes deployment in `README.md`.
  - Included image reference: `harbor.andreybondarenko.com/library/connectivity-exporter:latest`.

## 2025-05-15 – `d7ad566` by Andrey Bondarenko
- **Documentation Update**
  - Changed target port for `connectivity-exporter` from `8443` to `9090` in `README.md`.

## 2025-05-15 – `a8addf9` by Andrey Bondarenko
- **Configuration Update**: 
  - Changed default `PORT` from `9000` to `9090` in `README.md`. 
- **Documentation**: 
  - Updated environment variable instructions in `README.md`.

## 2025-05-16 – `b9fd5df` by Andrey Bondarenko
- **Flask Integration**: Added Flask web server to `connectivity-exporter.py` for serving status and metrics.
- **New Routes**:
  - `/`: Displays a status page with endpoint health and response times.
  - `/metrics`: Exposes Prometheus metrics using `generate_latest()`.
- **Status Management**: Introduced `endpoint_status` dictionary to track and display the status of monitored endpoints.
- **Threading**: Updated `main()` to run Flask app alongside the existing check loop.
- **Breaking Change**: The script now serves an HTTP server on the specified port, replacing the previous behavior of only starting a Prometheus metrics server.

## 2025-06-02 – `f2f7b35` by fossabot
- **Documentation Updates**
  - Added FOSSA status badge to README.md for license compliance visibility.
  - Introduced a new License section in README.md.

## 2025-07-08 – `1bfc7c5` by Andrey Bondarenko
- **CI/CD Workflow**: 
  - Added new GitHub Actions workflow for Docker image publishing in `.github/workflows/docker-publish.yml`.
  - Scheduled builds set to run daily at 2:29 AM UTC and on pushes to the `main` branch or version tags.

- **Docker Build Process**:
  - Integrated Docker Buildx for multi-platform image builds and caching.
  - Included steps for Docker metadata extraction and image signing using Cosign.

- **Permissions**:
  - Configured permissions for reading contents and writing packages in the workflow.

- **Conditional Execution**:
  - Steps for logging into the Docker registry and signing images are conditional on non-pull request events.

## 2025-07-08 – `914017b` by Andrey Bondarenko
- **New Feature**: Introduced `check.py` for connectivity checking with Prometheus metrics.
  - Implements HTTP endpoint checks with configurable intervals and expected status codes.
  - Provides a web interface to display connectivity status and metrics.

- **Removed**: Deleted `connectivity-exporter.py`.
  - All functionality has been migrated to `check.py`.

- **Configuration**: 
  - Added command-line arguments for port, interval, and config file path.
  - Config file must define endpoints for monitoring.

- **Metrics**: 
  - Integrates Prometheus metrics for connection status and response times.

- **Breaking Change**: 
  - Users must transition to `check.py` as the primary script; `connectivity-exporter.py` is no longer available.

## 2025-07-08 – `d2964dd` by Andrey Bondarenko
- **Dockerfile Updates:**
  - Changed working directory setup; commented out `WORKDIR /app`.
  - Updated file copy paths: `check.py` and `config.yaml` now copied to `/app` instead of current directory.
- **Permissions:**
  - Ensured `/etc/run` is executable with `chmod +x`.
