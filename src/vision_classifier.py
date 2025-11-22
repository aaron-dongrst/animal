"""
Vision Classifier for ZooGuardian
Maps action labels to health categories ("Healthy" or "Not Healthy").
"""

class VisionClassifier:
    """
    Classifies actions as "Healthy" or "Not Healthy" based on predefined mappings.
    """
    
    def __init__(self):
        # Define mappings of action labels to health categories
        self.label_to_health = {
            "eating carrots": "Healthy",
            "walking": "Healthy",
            "sleeping": "Healthy",
            "limping": "Not Healthy",
            "not eating": "Not Healthy",
            "agitated": "Not Healthy"
        }
    
    def classify_action(self, action_label: str) -> str:
        """
        Classify an action label as "Healthy" or "Not Healthy".
        
        Args:
            action_label: The action label to classify.
            
        Returns:
            Health category ("Healthy" or "Not Healthy").
        """
        return self.label_to_health.get(action_label, "Unknown")
