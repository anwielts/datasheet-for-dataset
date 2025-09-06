"""Template generation for datasheet questionnaires."""
from typing import Dict, List, Any, Optional
from pathlib import Path
import re
from .layout import BaseLayout
from .structures import DatasheetSection


class DatasheetTemplate:
    """Generates empty datasheet questionnaire templates based on the 'Datasheets for Datasets' paper.
    
    This class creates structured markdown templates that serve as blueprints for
    dataset documentation following the standardized datasheet format.
    """
    
    def __init__(self, layout: Optional[BaseLayout] = None):
        """Initialize the template generator with template directory path and optional layout.
        
        Args:
            layout: Optional BaseLayout instance to define section order and validation.
                   If not provided, uses default layout.
        """
        self.template_dir = Path(__file__).parent / "templates"
        
        if layout is None:
            self.layout = BaseLayout()
        else:
            self.layout = layout
        
        # Extract section order from layout
        self.section_order = [section.value for section in self.layout.sections]
    
    def _load_template(self, template_name: str) -> str:
        """Load a template file from the templates directory.
        
        Args:
            template_name: Name of the template file (without .md extension).
            
        Returns:
            str: Content of the template file.
        """
        template_path = self.template_dir / f"{template_name}.md"
        if not template_path.exists():
            raise FileNotFoundError(f"Template file not found: {template_path}")
        return template_path.read_text(encoding='utf-8')
    
    def generate_empty_template(self) -> str:
        """Generate an empty markdown template for datasheet questionnaire.
        
        Returns:
            str: Complete markdown template with all sections and questions.
        """
        template_parts = []
        
        # Add header
        template_parts.append(self._load_template("header"))
        
        # Add all sections in order
        for section_name in self.section_order:
            section_content = self._load_template(section_name)
            template_parts.append(section_content)
            template_parts.append("\n---\n")
        
        # Add footer
        template_parts.append(self._load_template("footer"))
        
        return "\n".join(template_parts)
    
    def get_section_names(self) -> List[str]:
        """Get list of all section names.
        
        Returns:
            List[str]: Names of all sections in the template.
        """
        return self.section_order.copy()
    
    def get_required_sections(self) -> List[str]:
        """Get list of required section names from the layout.
        
        Returns:
            List[str]: Names of all required sections.
        """
        return [section.value for section in self.layout.required_sections]
    
    def get_subsection_names(self, section: str) -> List[str]:
        """Get list of subsection names for a given section.
        
        Args:
            section: Name of the section.
            
        Returns:
            List[str]: Names of all subsections in the given section.
        """
        try:
            template_content = self._load_template(section)
            # Extract subsection headings (## headings) from the markdown content
            subsection_pattern = r'^## (.+)$'
            matches = re.findall(subsection_pattern, template_content, re.MULTILINE)
            return matches
        except FileNotFoundError:
            # Return empty list if template file doesn't exist
            return []