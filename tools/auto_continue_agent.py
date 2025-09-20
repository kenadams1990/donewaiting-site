#!/usr/bin/env python3
"""
Auto Continue Agent Script

A robust agent continuation script with proper error handling,
validation, and debugging capabilities.
"""

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
import subprocess
import signal


class AgentError(Exception):
    """Custom exception for agent-related errors"""
    pass


class AutoContinueAgent:
    """
    Robust agent continuation with error handling and validation
    """
    
    def __init__(self, role: str, pr_number: Optional[str] = None, debug: bool = False):
        self.role = role
        self.pr_number = pr_number
        self.debug = debug
        self.start_time = time.time()
        
        # Setup logging
        self._setup_logging()
        
        # Validate environment
        self._validate_environment()
        
        self.logger.info(f"Initialized AutoContinueAgent for role: {role}")
        
    def _setup_logging(self):
        """Setup robust logging configuration"""
        log_level = logging.DEBUG if self.debug else logging.INFO
        
        # Create logs directory if it doesn't exist
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        # Configure logging format
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        
        # Setup file handler
        log_file = logs_dir / f"agent_{self.role}_{int(time.time())}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(logging.Formatter(log_format))
        
        # Setup console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(logging.Formatter(log_format))
        
        # Configure logger
        self.logger = logging.getLogger(f"agent_{self.role}")
        self.logger.setLevel(log_level)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Prevent duplicate logs
        self.logger.propagate = False
        
    def _validate_environment(self):
        """Validate the environment and required dependencies"""
        self.logger.info("Validating environment...")
        
        # Check Python version
        python_version = sys.version_info
        if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
            raise AgentError(f"Python 3.8+ required, got {python_version.major}.{python_version.minor}")
        
        self.logger.info(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # Check required environment variables
        required_env_vars = []
        missing_vars = []
        
        for var in required_env_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            self.logger.warning(f"Missing environment variables: {missing_vars}")
        
        # Check required tools
        required_tools = ["git", "curl"]
        missing_tools = []
        
        for tool in required_tools:
            try:
                subprocess.run([tool, "--version"], 
                             capture_output=True, 
                             check=True, 
                             timeout=10)
                self.logger.debug(f"Tool {tool} is available")
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
                missing_tools.append(tool)
        
        if missing_tools:
            self.logger.error(f"Missing required tools: {missing_tools}")
            raise AgentError(f"Required tools not available: {missing_tools}")
        
        self.logger.info("Environment validation completed successfully")
    
    def _load_role_config(self) -> Dict[str, Any]:
        """Load role configuration with fallback defaults"""
        self.logger.info(f"Loading configuration for role: {self.role}")
        
        # Possible role file locations
        role_file_paths = [
            f"roles/{self.role}.yml",
            f"roles/{self.role}.yaml",
            f".github/roles/{self.role}.yml",
            f".github/roles/{self.role}.yaml",
            f"config/roles/{self.role}.yml",
            f"config/roles/{self.role}.yaml",
        ]
        
        config = {}
        config_loaded = False
        
        for path in role_file_paths:
            if Path(path).exists():
                try:
                    import yaml
                    with open(path, 'r') as f:
                        config = yaml.safe_load(f) or {}
                    self.logger.info(f"Loaded role config from: {path}")
                    config_loaded = True
                    break
                except Exception as e:
                    self.logger.warning(f"Failed to load config from {path}: {e}")
        
        if not config_loaded:
            self.logger.warning(f"No configuration file found for role {self.role}, using defaults")
        
        # Default configuration
        default_config = {
            "name": self.role,
            "description": f"Agent role: {self.role}",
            "timeout": 300,
            "retry_count": 3,
            "capabilities": ["basic"],
            "config": {
                "max_iterations": 10,
                "error_threshold": 5,
                "cooldown_seconds": 5
            }
        }
        
        # Merge with defaults
        for key, value in default_config.items():
            if key not in config:
                config[key] = value
        
        self.logger.debug(f"Final configuration: {json.dumps(config, indent=2)}")
        return config
    
    def _handle_signal(self, signum, frame):
        """Handle signals gracefully"""
        self.logger.warning(f"Received signal {signum}, initiating graceful shutdown...")
        self._cleanup()
        sys.exit(1)
    
    def _cleanup(self):
        """Cleanup resources and temporary files"""
        self.logger.info("Performing cleanup...")
        
        # Clean up any temporary files or resources
        temp_files = []
        for temp_file in temp_files:
            try:
                if Path(temp_file).exists():
                    Path(temp_file).unlink()
                    self.logger.debug(f"Cleaned up temporary file: {temp_file}")
            except Exception as e:
                self.logger.warning(f"Failed to cleanup {temp_file}: {e}")
        
        elapsed_time = time.time() - self.start_time
        self.logger.info(f"Agent ran for {elapsed_time:.2f} seconds")
    
    def _execute_with_retry(self, func, max_retries: int = 3, backoff_factor: float = 2.0):
        """Execute a function with retry logic and exponential backoff"""
        for attempt in range(max_retries):
            try:
                return func()
            except Exception as e:
                self.logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise
                
                sleep_time = backoff_factor ** attempt
                self.logger.info(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
    
    def _simulate_agent_work(self, config: Dict[str, Any]):
        """Simulate agent work based on role and configuration"""
        self.logger.info(f"Starting agent work for role: {self.role}")
        
        max_iterations = config.get("config", {}).get("max_iterations", 10)
        cooldown = config.get("config", {}).get("cooldown_seconds", 5)
        
        for iteration in range(max_iterations):
            self.logger.info(f"Iteration {iteration + 1}/{max_iterations}")
            
            # Simulate different types of work based on role
            if self.role == "code-reviewer":
                self._simulate_code_review()
            elif self.role == "documentation":
                self._simulate_documentation_work()
            elif self.role == "testing":
                self._simulate_testing_work()
            else:
                self._simulate_generic_work()
            
            if iteration < max_iterations - 1:
                self.logger.debug(f"Cooling down for {cooldown} seconds...")
                time.sleep(cooldown)
        
        self.logger.info("Agent work completed successfully")
    
    def _simulate_code_review(self):
        """Simulate code review work"""
        self.logger.info("Performing code review analysis...")
        
        # Simulate checking files
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", "HEAD~1..HEAD"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                files = result.stdout.strip().split('\n') if result.stdout.strip() else []
                self.logger.info(f"Found {len(files)} changed files to review")
                for file in files[:5]:  # Limit output
                    self.logger.debug(f"Reviewing file: {file}")
            else:
                self.logger.warning("Could not get list of changed files")
                
        except subprocess.TimeoutExpired:
            self.logger.warning("Git diff command timed out")
        except Exception as e:
            self.logger.warning(f"Error during code review simulation: {e}")
    
    def _simulate_documentation_work(self):
        """Simulate documentation work"""
        self.logger.info("Analyzing documentation needs...")
        
        # Check for common documentation files
        doc_files = ["README.md", "CONTRIBUTING.md", "docs/", "documentation/"]
        found_docs = []
        
        for doc in doc_files:
            if Path(doc).exists():
                found_docs.append(doc)
        
        self.logger.info(f"Found {len(found_docs)} documentation files/directories")
        
        # Simulate documentation analysis
        time.sleep(2)  # Simulate work
        self.logger.info("Documentation analysis completed")
    
    def _simulate_testing_work(self):
        """Simulate testing work"""
        self.logger.info("Analyzing test coverage and quality...")
        
        # Look for test files
        test_patterns = ["test_*.py", "*_test.py", "tests/", "test/"]
        found_tests = []
        
        for pattern in test_patterns:
            if "*" in pattern:
                # Simple glob simulation
                continue
            if Path(pattern).exists():
                found_tests.append(pattern)
        
        self.logger.info(f"Found {len(found_tests)} test files/directories")
        
        # Simulate test execution
        time.sleep(3)  # Simulate work
        self.logger.info("Test analysis completed")
    
    def _simulate_generic_work(self):
        """Simulate generic agent work"""
        self.logger.info("Performing generic agent analysis...")
        time.sleep(1)  # Simulate work
        self.logger.info("Generic analysis completed")
    
    def run(self):
        """Main execution method with comprehensive error handling"""
        try:
            # Setup signal handlers
            signal.signal(signal.SIGINT, self._handle_signal)
            signal.signal(signal.SIGTERM, self._handle_signal)
            
            self.logger.info(f"Starting AutoContinueAgent for role: {self.role}")
            
            # Load configuration
            config = self._execute_with_retry(self._load_role_config)
            
            # Execute main work
            self._execute_with_retry(
                lambda: self._simulate_agent_work(config),
                max_retries=config.get("retry_count", 3)
            )
            
            self.logger.info("Agent execution completed successfully")
            return 0
            
        except KeyboardInterrupt:
            self.logger.warning("Agent execution interrupted by user")
            return 130
        except AgentError as e:
            self.logger.error(f"Agent error: {e}")
            return 1
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}", exc_info=True)
            return 1
        finally:
            self._cleanup()
    
    @staticmethod
    def validate():
        """Validate that the agent script is properly configured"""
        print("Validating AutoContinueAgent...")
        
        # Check required imports
        required_modules = ["json", "logging", "os", "sys", "time", "pathlib", "subprocess", "signal"]
        missing_modules = []
        
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing_modules.append(module)
        
        if missing_modules:
            print(f"❌ Missing required modules: {missing_modules}")
            return False
        
        # Try importing optional modules
        try:
            import yaml
            print("✅ YAML module available")
        except ImportError:
            print("⚠️  YAML module not available, will use JSON fallback")
        
        print("✅ AutoContinueAgent validation passed")
        return True


def main():
    """Main entry point with argument parsing"""
    parser = argparse.ArgumentParser(
        description="Auto Continue Agent with robust error handling",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --role code-reviewer --pr-number 123
  %(prog)s --role documentation --debug
  %(prog)s --validate
        """
    )
    
    parser.add_argument(
        "--role",
        type=str,
        help="Agent role to execute (e.g., code-reviewer, documentation, testing)"
    )
    
    parser.add_argument(
        "--pr-number",
        type=str,
        help="Pull request number (if running in PR context)"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate agent configuration and dependencies"
    )
    
    args = parser.parse_args()
    
    # Handle validation mode
    if args.validate:
        success = AutoContinueAgent.validate()
        return 0 if success else 1
    
    # Require role for normal operation
    if not args.role:
        parser.error("--role is required (or use --validate)")
    
    try:
        agent = AutoContinueAgent(
            role=args.role,
            pr_number=args.pr_number,
            debug=args.debug
        )
        
        return agent.run()
        
    except Exception as e:
        print(f"Failed to initialize agent: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())