#!/usr/bin/env python3
"""
AGI Sentinel CSV Scanner - Enhanced
Professional CSV scanning with proper error handling
"""

import sys
import pandas as pd
from pathlib import Path

# Correct import (FIXED from original error)
from src.agi_sentinel.core import AGISentinel

def scan_csv(
    file_path: str,
    col_names: list = None,
    output_suffix: str = "_shielded",
    verbose: bool = False
):
    """
    Scan CSV file with professional error handling
    
    Args:
        file_path: Path to CSV file
        col_names: List of column names to scan (None for all)
        output_suffix: Suffix for output file
        verbose: Print detailed progress
    
    Returns:
        Path to output file or None if failed
    """
    file_path = Path(file_path)
    
    # Validation
    if not file_path.exists():
        print(f"[ERROR] File not found: {file_path}", file=sys.stderr)
        return None
    
    if file_path.suffix.lower() != '.csv':
        print(f"[ERROR] Not a CSV file: {file_path}", file=sys.stderr)
        return None
    
    try:
        # Initialize sentinel
        guard = AGISentinel()
        
        if verbose:
            print(f"[*] Loading {file_path}...")
        
        # Read CSV
        df = pd.read_csv(file_path)
        
        if verbose:
            print(f"[*] Loaded {len(df)} rows, {len(df.columns)} columns")
        
        # Determine columns to scan
        if col_names is None:
            col_names = df.columns.tolist()
        
        # Validate columns exist
        missing_cols = [col for col in col_names if col not in df.columns]
        if missing_cols:
            print(f"[ERROR] Columns not found: {', '.join(missing_cols)}", file=sys.stderr)
            return None
        
        if verbose:
            print(f"[*] Scanning columns: {', '.join(col_names)}")
        
        # Scan each column
        for col in col_names:
            if verbose:
                print(f"[*] Processing column: {col}")
            
            # Apply protection
            df[f'{col}_shielded'] = df[col].astype(str).apply(
                lambda x: guard.protect(x)['output']
            )
        
        # Generate output filename
        output_file = file_path.parent / f"{file_path.stem}{output_suffix}{file_path.suffix}"
        
        # Save results
        df.to_csv(output_file, index=False)
        
        if verbose:
            print(f"[+] Scan complete! Results saved to: {output_file}")
            print(f"[+] Original columns: {len(df.columns) - len(col_names)}")
            print(f"[+] New shielded columns: {len(col_names)}")
        
        return output_file
    
    except pd.errors.EmptyDataError:
        print(f"[ERROR] CSV file is empty: {file_path}", file=sys.stderr)
        return None
    except pd.errors.ParserError as e:
        print(f"[ERROR] Failed to parse CSV: {e}", file=sys.stderr)
        return None
    except MemoryError:
        print(f"[ERROR] File too large for memory: {file_path}", file=sys.stderr)
        print("[TIP] Use the main CLI with --chunk-size for large files", file=sys.stderr)
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}", file=sys.stderr)
        return None

def main():
    """Command line interface for CSV scanning"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="AGI Sentinel CSV Scanner",
        epilog="Example: python scan_csv.py data.csv --cols email phone --verbose"
    )
    
    parser.add_argument(
        "csv_file",
        help="CSV file to scan"
    )
    
    parser.add_argument(
        "--cols", "-c",
        nargs='+',
        help="Columns to scan (default: all columns)",
        default=None
    )
    
    parser.add_argument(
        "--output", "-o",
        help="Output file name (default: original_shielded.csv)",
        default=None
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    # Execute scan

result = scan_csv(
        file_path=args.csv_file,
        col_names=args.cols,
        output_suffix="",
        verbose=args.verbose
    )
    
    if result:
        # Rename if output specified
        if args.output:
            import shutil
            shutil.move(str(result), args.output)
            print(f"[+] Final output: {args.output}")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
