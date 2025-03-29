from datetime import datetime
import json
import os

class SessionContext:
    def __init__(self, session_id=None, max_history=10):
        """
        Initialize session context with optional existing session ID
        
        Args:
            session_id (str, optional): Session identifier
            max_history (int): Maximum number of interactions to store
        """
        self.session_id = session_id or self._generate_session_id()
        self.max_history = max_history
        self.interaction_history = []
        self.session_data = {}
        
        # Create sessions directory if it doesn't exist
        os.makedirs('sessions', exist_ok=True)
        
        # Load existing session if available
        self._load_session()
    
    def _generate_session_id(self):
        """Generate a unique session ID"""
        return f"session_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def _load_session(self):
        """Load session from disk if it exists"""
        session_file = f"sessions/{self.session_id}.json"
        if os.path.exists(session_file):
            try:
                with open(session_file, 'r') as f:
                    data = json.load(f)
                    self.interaction_history = data.get('history', [])
                    self.session_data = data.get('data', {})
            except Exception:
                # If loading fails, start with empty session
                pass
    
    def _save_session(self):
        """Save session to disk"""
        session_file = f"sessions/{self.session_id}.json"
        data = {
            'history': self.interaction_history,
            'data': self.session_data
        }
        
        with open(session_file, 'w') as f:
            json.dump(data, f)
    
    def add_interaction(self, user_query, response, metadata=None):
        """
        Add an interaction to the session history
        
        Args:
            user_query (str): User's query/prompt
            response (dict): System response
            metadata (dict, optional): Additional metadata about the interaction
        """
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'user_query': user_query,
            'response': response,
            'metadata': metadata or {}
        }
        
        # Add to history and limit size
        self.interaction_history.append(interaction)
        if len(self.interaction_history) > self.max_history:
            self.interaction_history = self.interaction_history[-self.max_history:]
        
        # Save session
        self._save_session()
    
    def set_data(self, key, value):
        """Store data in the session"""
        self.session_data[key] = value
        self._save_session()
    
    def get_data(self, key, default=None):
        """Retrieve data from the session"""
        return self.session_data.get(key, default)
    
    def get_context_summary(self):
        """
        Generate a summary of recent interactions for context
        
        Returns:
            str: Summary of recent interactions
        """
        if not self.interaction_history:
            return "No previous interactions."
        
        summary = []
        for i, interaction in enumerate(self.interaction_history[-3:]):  # Last 3 interactions
            timestamp = datetime.fromisoformat(interaction['timestamp']).strftime('%H:%M:%S')
            summary.append(f"Interaction {i+1} ({timestamp}):")
            summary.append(f"User: {interaction['user_query']}")
            
            # Simplified response summary
            response = interaction['response']
            if isinstance(response, dict):
                if 'function' in response:
                    summary.append(f"System: Used function '{response['function']}'")
                elif 'error' in response:
                    summary.append(f"System: Error - {response['error']}")
                else:
                    summary.append("System: Response provided")
            else:
                summary.append("System: Response provided")
            
            summary.append("---")
        
        return "\n".join(summary)