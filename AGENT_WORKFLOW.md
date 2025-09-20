# Agent PR Matrix Workflow

This document describes the robust Agent PR Matrix workflow that provides enhanced error handling, debugging capabilities, and resilient operation.

## Overview

The `agent-pr-matrix.yml` workflow is designed to run multiple agent roles in parallel when pull requests are created or updated. It includes comprehensive error handling, validation, and debugging features.

## Features

### 🛡️ Error Handling & Resilience
- **Graceful failure handling**: Individual agent failures don't stop the entire workflow
- **Retry logic**: Automatic retry with exponential backoff for transient failures
- **Timeout protection**: Configurable timeouts prevent hung processes
- **Signal handling**: Proper cleanup on interruption

### 🔍 Debugging & Monitoring
- **Comprehensive logging**: Detailed logs for troubleshooting
- **Validation steps**: Pre-flight checks for tools and configuration
- **Progress tracking**: Clear status reporting throughout execution
- **Artifact collection**: Automatic log collection for post-mortem analysis

### ⚙️ Configuration & Flexibility
- **Role detection**: Automatic discovery of role configuration files
- **Fallback defaults**: Sensible defaults when configuration is missing
- **Matrix-based execution**: Parallel execution of multiple agent roles
- **Environment validation**: Pre-execution validation of required tools

## Workflow Structure

### 1. Setup Job
- **Environment validation**: Checks Python version, required tools
- **Role detection**: Discovers available role configurations
- **Tool validation**: Validates the `auto_continue_agent.py` script
- **Matrix generation**: Creates execution matrix based on available roles

### 2. Agent Jobs
- **Parallel execution**: Runs multiple agent roles simultaneously
- **Error isolation**: Individual job failures don't affect others
- **Resource monitoring**: Tracks memory and disk usage
- **Log collection**: Captures detailed execution logs

### 3. Summary Job
- **Status reporting**: Aggregates results from all jobs
- **Artifact management**: Organizes logs and outputs
- **Final reporting**: Provides comprehensive summary

## Agent Script (`tools/auto_continue_agent.py`)

### Key Features
- **Modular design**: Easily extensible for new agent types
- **Robust error handling**: Comprehensive exception handling
- **Configuration management**: Flexible role-based configuration
- **Resource cleanup**: Proper cleanup of temporary resources
- **Signal handling**: Graceful shutdown on interruption

### Supported Agent Roles
- **code-reviewer**: Analyzes code changes and provides feedback
- **documentation**: Reviews and suggests documentation improvements
- **testing**: Analyzes test coverage and quality
- **generic**: Fallback for custom roles

### Configuration

Role configurations are loaded from:
1. `roles/{role}.yml`
2. `roles/{role}.yaml`
3. `.github/roles/{role}.yml`
4. `.github/roles/{role}.yaml`
5. `config/roles/{role}.yml`
6. `config/roles/{role}.yaml`

Example role configuration:
```yaml
name: "code-reviewer"
description: "Automated code review agent"
capabilities:
  - code_analysis
  - security_scan
  - style_check
config:
  timeout: 600
  retry_count: 2
  max_iterations: 5
  cooldown_seconds: 3
```

## Usage

### Triggering the Workflow
The workflow runs automatically on:
- Pull request opened
- Pull request synchronized (new commits)
- Pull request reopened

Manual trigger with debug mode:
```yaml
workflow_dispatch:
  inputs:
    debug:
      description: 'Enable debug mode'
      type: boolean
      default: false
```

### Running the Agent Script Manually
```bash
# Validate the agent
python tools/auto_continue_agent.py --validate

# Run specific role
python tools/auto_continue_agent.py --role code-reviewer --pr-number 123

# Debug mode
python tools/auto_continue_agent.py --role testing --debug
```

## Error Handling Scenarios

### 1. Missing Dependencies
- **Detection**: Pre-flight validation checks for required tools
- **Response**: Clear error messages with installation instructions
- **Fallback**: Graceful degradation where possible

### 2. Configuration Issues
- **Detection**: YAML syntax validation and schema checking
- **Response**: Use sensible defaults for missing configuration
- **Logging**: Detailed warnings about configuration issues

### 3. Resource Constraints
- **Detection**: Memory and disk space monitoring
- **Response**: Cleanup of temporary files and resources
- **Prevention**: Configurable timeouts and limits

### 4. Network Issues
- **Detection**: Timeout-based detection of network problems
- **Response**: Retry logic with exponential backoff
- **Fallback**: Local-only operation where possible

## Monitoring and Troubleshooting

### Log Locations
- **Workflow logs**: Available in GitHub Actions interface
- **Agent logs**: Collected as artifacts in `logs/` directory
- **Individual job logs**: Named by role (e.g., `agent-code-reviewer.log`)

### Common Issues

#### "No role files detected"
- **Cause**: Missing role configuration files
- **Solution**: Create role files in supported locations
- **Workaround**: Default configuration is automatically created

#### "Tools validation failed"
- **Cause**: Missing required command-line tools
- **Solution**: Ensure git, curl, and other tools are available
- **Check**: Run validation step manually

#### "Agent execution timeout"
- **Cause**: Agent taking longer than configured timeout
- **Solution**: Increase timeout in role configuration
- **Debug**: Enable debug mode for detailed logging

### Debug Mode
Enable debug mode for verbose logging:
- **Workflow**: Set debug input to `true`
- **Script**: Use `--debug` flag
- **Logs**: Include detailed timing and state information

## Best Practices

### Role Configuration
1. **Specific timeouts**: Set appropriate timeouts for each role
2. **Resource limits**: Configure memory and CPU limits
3. **Error thresholds**: Define acceptable failure rates
4. **Retry policies**: Configure retry behavior per role

### Error Handling
1. **Fail fast**: Detect issues early in the process
2. **Graceful degradation**: Continue operation when possible
3. **Clear messaging**: Provide actionable error messages
4. **Resource cleanup**: Always clean up temporary resources

### Monitoring
1. **Regular validation**: Periodically test the workflow
2. **Log analysis**: Review logs for patterns and issues
3. **Performance monitoring**: Track execution times and resource usage
4. **Alert setup**: Configure notifications for critical failures

## Contributing

When modifying the workflow or agent script:

1. **Test thoroughly**: Validate changes in development environment
2. **Update documentation**: Keep this guide current with changes
3. **Maintain backwards compatibility**: Preserve existing functionality
4. **Add tests**: Include validation for new features
5. **Review error handling**: Ensure robust error handling for new code paths