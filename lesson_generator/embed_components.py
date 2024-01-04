# lesson_generator/embed_components.py

from lesson_generator.component_mapping import get_mdx_representation

def wrap_content_with_components(content, components):
    """Embeds React components within the MDX content according to the components list."""
    for component in components:
        content = get_mdx_representation(component, content)
    return content

def embed_components_in_sections(lessons_data):
    """Embeds React components within each section's generated content."""
    for lesson in lessons_data:
        for section in lesson['sections']:
            components = section.get('components', [])
            if components:
                content_with_components = wrap_content_with_components(
                    section['generated_content'],
                    components
                )
                section['generated_content'] = content_with_components
    return lessons_data
