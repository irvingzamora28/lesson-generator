# lesson_generator/component_mapping.py

# Dictionary to map component names to their MDX representation
COMPONENT_MDX_MAPPING = {
    "TextToSpeechPlayer": "<TextToSpeechPlayer>{content}</TextToSpeechPlayer>",
    "TipBox": "<TipBox>{content}</TipBox>",
    "Mnemonic": "<Mnemonic>{content}</Mnemonic>"
}

def get_mdx_representation(component_name, content):
    """Returns the MDX representation for a given component with content."""
    if component_name not in COMPONENT_MDX_MAPPING:
        raise ValueError(f"No MDX mapping found for component: {component_name}")
    
    return COMPONENT_MDX_MAPPING[component_name].format(content=content)
