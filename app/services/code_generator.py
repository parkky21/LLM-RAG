import re
import inspect
from app.services.llm import LLMService

class CodeGenerator:
    def __init__(self):
        self.llm = LLMService()
    
    def generate_function_code(self, function_info, user_input=None):
        """
        Generate executable Python code for a function
        
        Args:
            function_info (dict): Information about the function
            user_input (str, optional): Original user query for context
            
        Returns:
            str: Generated Python code
        """
        # Extract function details
        module_name = function_info['module']
        function_name = function_info['name']
        
        # Parse function signature to extract parameters
        signature_str = function_info['signature']
        params = self._parse_parameters(signature_str)
        param_values = self._extract_parameter_values(user_input, params)
        
        # Generate code template
        code = f"""from app.functions.{module_name} import {function_name}

def main():
    try:
        # Execute the function
        result = {function_name}({self._format_arguments(param_values)})
        
        # Handle the result
        if result is None:
            print("Function executed successfully with no return value.")
        elif isinstance(result, bool):
            status = "successfully" if result else "with issues"
""" + r""""
            print(f"Function executed {status}.")
        elif isinstance(result, dict):
            print("Function result:")
            for key, value in result.items():
                print(f"  {key}: {value}")
        else:
            print(f"Result: {result}")
            
    except Exception as e:
        print(f"Error executing function: {e}")

if __name__ == "__main__":
    main()
"""
        return code
    
    def _parse_parameters(self, signature_str):
        """Parse function signature to extract parameters"""
        params = []
        # Remove parentheses and split parameters
        if '(' in signature_str and ')' in signature_str:
            param_str = signature_str.split('(', 1)[1].rsplit(')', 1)[0]
            
            # Handle empty parameter list
            if not param_str.strip():
                return params
                
            # Split by comma, but respect nested structures
            depth = 0
            current = ""
            for char in param_str + ',':
                if char == ',' and depth == 0:
                    if current.strip():
                        params.append(current.strip())
                    current = ""
                    continue
                elif char == '(':
                    depth += 1
                elif char == ')':
                    depth -= 1
                current += char
        
        # Process each parameter
        processed_params = []
        for p in params:
            # Check for default value
            has_default = '=' in p
            name = p.split('=', 1)[0].strip() if has_default else p.strip()
            default = p.split('=', 1)[1].strip() if has_default else None
            
            # Remove type hints if present
            if ':' in name:
                name = name.split(':', 1)[0].strip()
                
            processed_params.append({
                'name': name,
                'has_default': has_default,
                'default': default
            })
            
        return processed_params
    
    def _extract_parameter_values(self, user_input, params):
        """Extract parameter values from user input"""
        param_values = {}
        
        if not user_input or not params:
            return param_values
            
        # Use regex to try to extract parameter values from user input
        for param in params:
            name = param['name']
            # Skip 'self' parameter
            if name == 'self':
                continue
                
            # Look for patterns like "with url google.com" or "url: google.com"
            patterns = [
                rf"(?:with|using|for)\s+{name}\s+(?:of|as|:)?\s+([^,\.]+)",
                rf"{name}(?:\s+is|:)\s+([^,\.]+)",
                rf"(?:set|using)\s+{name}\s+(?:to|as)\s+([^,\.]+)"
            ]
            
            for pattern in patterns:
                matches = re.search(pattern, user_input, re.IGNORECASE)
                if matches:
                    param_values[name] = matches.group(1).strip()
                    break
        
        return param_values
    
    def _format_arguments(self, param_values):
        """Format arguments for function call"""
        args = []
        for name, value in param_values.items():
            # Check if value is a string that should be quoted
            if value.isdigit():
                args.append(f"{name}={value}")
            elif value.lower() in ('true', 'false', 'none'):
                args.append(f"{name}={value.capitalize()}")
            else:
                args.append(f'{name}="{value}"')
        
        return ", ".join(args)
