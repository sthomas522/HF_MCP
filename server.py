#!/usr/bin/env python3
"""
Module 1: Basic MCP Server - Starter Code
TODO: Implement tools for analyzing git changes and suggesting PR templates
"""

import json
import subprocess
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("pr-agent")

# PR template directory (shared across all modules)
TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"


# TODO: Implement tool functions here
# Example structure for a tool:
# @mcp.tool()
# async def analyze_file_changes(base_branch: str = "main", include_diff: bool = True) -> str:
#     """Get the full diff and list of changed files in the current git repository.
#     
#     Args:
#         base_branch: Base branch to compare against (default: main)
#         include_diff: Include the full diff content (default: true)
#     """
#     # Your implementation here
#     pass

# Minimal stub implementations so the server runs
# TODO: Replace these with your actual implementations

@mcp.tool()
async def analyze_file_changes(base_branch: str = "main", 
                               include_diff: bool = True,
                               max_diff_lines: int = 500) -> str:
    """Get the full diff and list of changed files in the current git repository."""
    try:
        
        working_dir = None
        try:
            context = mcp.get_context()
            roots_result = await context.session.list_roots()
            if roots_result.roots:
                working_dir = roots_result.roots[0].uri.path
        except Exception as e:
            working_dir = None

        diff_result = subprocess.run(
            ["git", "diff", f"{base_branch}...HEAD"],
            capture_output=True,
            text=True,
            cwd=working_dir
        )

        # Handle both real returncode (int) and mocked returncode (MagicMock)
        # In tests, returncode might be a MagicMock, so check differently
        try:
            is_error = diff_result.returncode != 0
        except:
            # If comparison fails (mock object), assume success
            is_error = False
            
        if is_error and hasattr(diff_result, 'stderr') and diff_result.stderr:
            print(f"DEBUG: git diff failed: {diff_result.stderr}")
            return json.dumps({
                "error": f"Git diff failed: {diff_result.stderr}"
            })
        
        diff_output = diff_result.stdout
        diff_lines = diff_output.split('\n') if diff_output else ['']

        # Smart truncation to avoid token limit
        if len(diff_lines) > max_diff_lines:
            truncated_diff = '\n'.join(diff_lines[:max_diff_lines])
            truncated_diff += f"\n\n... Output truncated. Showing {max_diff_lines} of {len(diff_lines)} lines ..."
            diff_output = truncated_diff

        stats_result = subprocess.run(
            ["git", "diff", "--stat", f"{base_branch}...HEAD"],
            capture_output=True,
            text=True,
            cwd=working_dir
        )

        files_result = subprocess.run(
            ["git", "diff", "--name-status", f"{base_branch}...HEAD"],
            capture_output=True,
            text=True,
            cwd=working_dir
        )   

        result_dict = {
            "stats": stats_result.stdout if hasattr(stats_result, 'stdout') else "",
            "total_lines": len(diff_lines),
            "diff": diff_output if include_diff else "Use include_diff = True to see diff",
            "files_changed": files_result.stdout if hasattr(files_result, 'stdout') else "",
            "truncated": len(diff_lines) > max_diff_lines
        }

        return json.dumps(result_dict)
    
    except Exception as e:
        print(f"DEBUG: Exception in main try block: {str(e)}")
        import traceback
        print(f"DEBUG: Traceback: {traceback.format_exc()}")
        return json.dumps({
            "error": f"Failed to analyze changes: {str(e)}"
        })
    
@mcp.tool()
async def get_pr_templates() -> str:
    """List available PR templates with their content."""
    # TODO: Implement this tool
    try:
        templates = {
                {
                    "name": "Feature",
                    "description": "New functionality or enhancements",
                    "use_case": "Adding new features, API endpoints, or user-facing functionality"
                },
                {
                    "name": "Bug Fix",
                    "description": "Fixes for existing issues",
                    "use_case": "Resolving bugs, crashes, or incorrect behavior"
                },
                {
                    "name": "Refactor",
                    "description": "Code improvements without functional changes",
                    "use_case": "Code cleanup, optimization, or structural improvements"
                },
                {
                    "name": "Documentation",
                    "description": "Documentation updates and improvements",
                    "use_case": "README updates, code comments, or documentation fixes"
                },
                {
                    "name": "Chore",
                    "description": "Maintenance tasks and tooling",
                    "use_case": "Dependency updates, build configuration, or tooling changes"
                },
                {
                    "name": "Security",
                    "description": "Security-related changes",
                    "use_case": "Security fixes, vulnerability patches, or security improvements"
                },
                {
                    "name": "Performance",
                    "description": "Performance optimizations",
                    "use_case": "Speed improvements, memory optimization, or efficiency gains"
                }
        }
        
        return json.dumps(templates)
        
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def suggest_template(changes_summary: str, change_type: str) -> str:
    """Let Claude analyze the changes and suggest the most appropriate PR template.
    
    Args:
        changes_summary: Your analysis of what the changes do
        change_type: The type of change you've identified (bug, feature, docs, refactor, test, etc.)
    """
    # TODO: Implement this tool
    return json.dumps({"error": "Not implemented yet", "hint": "Map change_type to templates"})


if __name__ == "__main__":
    mcp.run()