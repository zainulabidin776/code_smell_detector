"""
Code Smell Detection Application
Authors: Yusuf & Ahmed
Detects 6 common code smells in Python source code
"""

import ast
import re
import yaml
import argparse
from collections import defaultdict
from pathlib import Path


class CodeSmellDetector:
    """Main detector class that analyzes Python source code for code smells"""
    
    def __init__(self, config_file='config.yaml'):
        self.config = self.load_config(config_file)
        self.results = {
            'LongMethod': [],
            'GodClass': [],
            'DuplicatedCode': [],
            'LargeParameterList': [],
            'MagicNumbers': [],
            'FeatureEnvy': []
        }
        self.active_smells = []
    
    def load_config(self, config_file):
        """Load configuration from YAML file"""
        try:
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Warning: {config_file} not found. Using default configuration.")
            return self.get_default_config()
    
    def get_default_config(self):
        """Return default configuration"""
        return {
            'smells': {
                'LongMethod': {'enabled': True, 'max_lines': 50},
                'GodClass': {'enabled': True, 'max_methods': 15, 'max_attributes': 10},
                'DuplicatedCode': {'enabled': True, 'min_similarity': 0.8, 'min_lines': 5},
                'LargeParameterList': {'enabled': True, 'max_parameters': 5},
                'MagicNumbers': {'enabled': True, 'allowed_numbers': [0, 1, -1]},
                'FeatureEnvy': {'enabled': True, 'external_call_threshold': 0.6}
            }
        }
    
    def determine_active_smells(self, only_smells=None, exclude_smells=None):
        """Determine which smells to check based on CLI args and config"""
        all_smells = list(self.config['smells'].keys())
        
        if only_smells:
            self.active_smells = [s for s in only_smells.split(',') if s in all_smells]
        elif exclude_smells:
            excluded = exclude_smells.split(',')
            self.active_smells = [s for s in all_smells if s not in excluded]
        else:
            self.active_smells = [s for s in all_smells if self.config['smells'][s]['enabled']]
        
        return self.active_smells
    
    def analyze_file(self, filepath):
        """Analyze a Python file for code smells"""
        with open(filepath, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            print(f"Syntax error in {filepath}: {e}")
            return
        
        source_lines = source_code.split('\n')
        
        if 'LongMethod' in self.active_smells:
            self.detect_long_methods(tree, source_lines, filepath)
        
        if 'GodClass' in self.active_smells:
            self.detect_god_classes(tree, filepath)
        
        if 'DuplicatedCode' in self.active_smells:
            self.detect_duplicated_code(source_lines, filepath)
        
        if 'LargeParameterList' in self.active_smells:
            self.detect_large_parameter_lists(tree, filepath)
        
        if 'MagicNumbers' in self.active_smells:
            self.detect_magic_numbers(tree, source_lines, filepath)
        
        if 'FeatureEnvy' in self.active_smells:
            self.detect_feature_envy(tree, source_code, filepath)
    
    def detect_long_methods(self, tree, source_lines, filepath):
        """Detect methods that are too long"""
        max_lines = self.config['smells']['LongMethod']['max_lines']
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                start_line = node.lineno
                end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line
                method_lines = end_line - start_line + 1
                
                if method_lines > max_lines:
                    self.results['LongMethod'].append({
                        'file': filepath,
                        'method': node.name,
                        'lines': f"{start_line}-{end_line}",
                        'length': method_lines,
                        'threshold': max_lines,
                        'message': f"Method '{node.name}' has {method_lines} lines (threshold: {max_lines})"
                    })
    
    def detect_god_classes(self, tree, filepath):
        """Detect classes with too many responsibilities"""
        max_methods = self.config['smells']['GodClass']['max_methods']
        max_attributes = self.config['smells']['GodClass']['max_attributes']
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = [n for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
                
                # Count attributes initialized in __init__
                attributes = 0
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name == '__init__':
                        for stmt in ast.walk(item):
                            if isinstance(stmt, ast.Assign):
                                for target in stmt.targets:
                                    if isinstance(target, ast.Attribute):
                                        if isinstance(target.value, ast.Name) and target.value.id == 'self':
                                            attributes += 1
                
                if len(methods) > max_methods or attributes > max_attributes:
                    self.results['GodClass'].append({
                        'file': filepath,
                        'class': node.name,
                        'lines': f"{node.lineno}-{node.end_lineno if hasattr(node, 'end_lineno') else node.lineno}",
                        'methods': len(methods),
                        'attributes': attributes,
                        'message': f"Class '{node.name}' has {len(methods)} methods and {attributes} attributes (thresholds: {max_methods} methods, {max_attributes} attributes)"
                    })
    
    def detect_duplicated_code(self, source_lines, filepath):
        """Detect duplicated code blocks"""
        min_lines = self.config['smells']['DuplicatedCode']['min_lines']
        min_similarity = self.config['smells']['DuplicatedCode']['min_similarity']
        
        # Normalize lines (remove whitespace and comments)
        normalized_lines = []
        for line in source_lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                normalized_lines.append(stripped)
        
        # Find duplicated sequences
        duplicates_found = []
        for i in range(len(normalized_lines) - min_lines):
            for j in range(i + min_lines, len(normalized_lines) - min_lines):
                block1 = normalized_lines[i:i + min_lines]
                block2 = normalized_lines[j:j + min_lines]
                
                similarity = sum(1 for a, b in zip(block1, block2) if a == b) / len(block1)
                
                if similarity >= min_similarity:
                    # Check if not already reported
                    if not any(d['lines1'].startswith(str(i+1)) for d in duplicates_found):
                        duplicates_found.append({
                            'lines1': f"{i+1}-{i+min_lines}",
                            'lines2': f"{j+1}-{j+min_lines}",
                            'similarity': round(similarity * 100, 1)
                        })
        
        if duplicates_found:
            self.results['DuplicatedCode'].append({
                'file': filepath,
                'duplicates': duplicates_found,
                'message': f"Found {len(duplicates_found)} duplicated code block(s)"
            })
    
    def detect_large_parameter_lists(self, tree, filepath):
        """Detect methods with too many parameters"""
        max_params = self.config['smells']['LargeParameterList']['max_parameters']
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                param_count = len(node.args.args)
                # Don't count 'self' or 'cls'
                if param_count > 0 and node.args.args[0].arg in ['self', 'cls']:
                    param_count -= 1
                
                if param_count > max_params:
                    param_names = [arg.arg for arg in node.args.args]
                    self.results['LargeParameterList'].append({
                        'file': filepath,
                        'method': node.name,
                        'line': node.lineno,
                        'parameter_count': param_count,
                        'parameters': param_names,
                        'threshold': max_params,
                        'message': f"Method '{node.name}' has {param_count} parameters (threshold: {max_params})"
                    })
    
    def detect_magic_numbers(self, tree, source_lines, filepath):
        """Detect hard-coded numeric values"""
        allowed = self.config['smells']['MagicNumbers']['allowed_numbers']
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Num):
                if node.n not in allowed:
                    # Get context (function or class)
                    context = self.get_context_for_node(tree, node)
                    
                    self.results['MagicNumbers'].append({
                        'file': filepath,
                        'line': node.lineno,
                        'value': node.n,
                        'context': context,
                        'message': f"Magic number {node.n} found at line {node.lineno} in {context}"
                    })
            elif isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                if node.value not in allowed:
                    context = self.get_context_for_node(tree, node)
                    
                    self.results['MagicNumbers'].append({
                        'file': filepath,
                        'line': node.lineno,
                        'value': node.value,
                        'context': context,
                        'message': f"Magic number {node.value} found at line {node.lineno} in {context}"
                    })
    
    def get_context_for_node(self, tree, target_node):
        """Get the function or class context for a node"""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
                    if node.lineno <= target_node.lineno <= node.end_lineno:
                        return node.name
        return "module"
    
    def detect_feature_envy(self, tree, source_code, filepath):
        """Detect methods that use other classes' data more than their own"""
        threshold = self.config['smells']['FeatureEnvy']['external_call_threshold']
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Skip if not a method (no self parameter)
                if not node.args.args or node.args.args[0].arg != 'self':
                    continue
                
                self_accesses = 0
                external_accesses = 0
                
                for child in ast.walk(node):
                    if isinstance(child, ast.Attribute):
                        if isinstance(child.value, ast.Name):
                            if child.value.id == 'self':
                                self_accesses += 1
                            else:
                                external_accesses += 1
                
                total_accesses = self_accesses + external_accesses
                if total_accesses > 0:
                    external_ratio = external_accesses / total_accesses
                    
                    if external_ratio > threshold and external_accesses > 3:
                        self.results['FeatureEnvy'].append({
                            'file': filepath,
                            'method': node.name,
                            'line': node.lineno,
                            'self_accesses': self_accesses,
                            'external_accesses': external_accesses,
                            'ratio': round(external_ratio, 2),
                            'threshold': threshold,
                            'message': f"Method '{node.name}' accesses external data {external_accesses} times vs self {self_accesses} times (ratio: {external_ratio:.2f})"
                        })
    
    def generate_report(self):
        """Generate a formatted report of detected smells"""
        report = []
        report.append("=" * 80)
        report.append("CODE SMELL DETECTION REPORT")
        report.append("=" * 80)
        report.append(f"\nActive Smells Evaluated: {', '.join(self.active_smells)}\n")
        
        total_smells = sum(len(v) for v in self.results.values())
        report.append(f"Total Code Smells Found: {total_smells}\n")
        
        for smell_type in self.active_smells:
            smells = self.results[smell_type]
            if smells:
                report.append(f"\n{'-' * 80}")
                report.append(f"{smell_type}: {len(smells)} occurrence(s)")
                report.append(f"{'-' * 80}")
                
                for smell in smells:
                    report.append(f"\n  File: {smell.get('file', 'N/A')}")
                    report.append(f"  {smell['message']}")
                    
                    if 'lines' in smell:
                        report.append(f"  Lines: {smell['lines']}")
                    elif 'line' in smell:
                        report.append(f"  Line: {smell['line']}")
                    
                    if smell_type == 'DuplicatedCode' and 'duplicates' in smell:
                        for dup in smell['duplicates']:
                            report.append(f"    • Lines {dup['lines1']} duplicate Lines {dup['lines2']} ({dup['similarity']}% similar)")
        
        report.append(f"\n{'=' * 80}")
        return '\n'.join(report)
    
    def save_report(self, output_file='smell_report.txt'):
        """Save the report to a file"""
        report = self.generate_report()
        with open(output_file, 'w') as f:
            f.write(report)
        print(f"\nReport saved to {output_file}")
        return output_file


def main():
    """Main entry point for the code smell detector"""
    parser = argparse.ArgumentParser(description='Code Smell Detection Tool')
    parser.add_argument('files', nargs='+', help='Python files to analyze')
    parser.add_argument('--config', default='config.yaml', help='Configuration file (default: config.yaml)')
    parser.add_argument('--only', help='Only check specified smells (comma-separated)')
    parser.add_argument('--exclude', help='Exclude specified smells (comma-separated)')
    parser.add_argument('--output', default='smell_report.txt', help='Output report file')
    
    args = parser.parse_args()
    
    detector = CodeSmellDetector(args.config)
    detector.determine_active_smells(args.only, args.exclude)
    
    print(f"Analyzing {len(args.files)} file(s)...")
    print(f"Active smells: {', '.join(detector.active_smells)}\n")
    
    for filepath in args.files:
        if Path(filepath).exists():
            print(f"Analyzing: {filepath}")
            detector.analyze_file(filepath)
        else:
            print(f"Warning: File not found - {filepath}")
    
    print(detector.generate_report())
    detector.save_report(args.output)


if __name__ == '__main__':
    main()