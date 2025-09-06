"""Defines datasheet information cards for the datasheet structure."""
from typing import Optional, List, Dict, Any, TYPE_CHECKING
from pydantic import BaseModel, Field
from enum import Enum

from dfd.dataset.analyses import TabularStatistics

if TYPE_CHECKING:
    from dfd.datasheet.layout import BaseLayout


class CardType(str, Enum):
    """Types of datasheet information cards."""
    MANUAL = "manual"  # User-filled content
    AUTOMATED = "automated"  # System-generated content
    MIXED = "mixed"  # Combination of both


class DatasheetSection(str, Enum):
    """Standard datasheet sections based on the paper."""
    MOTIVATION = "motivation"
    COMPOSITION = "composition"
    COLLECTION_PROCESS = "collection_process"
    PREPROCESSING = "preprocessing"
    USES = "uses"
    DISTRIBUTION = "distribution"
    MAINTENANCE = "maintenance"
    AUTOMATED_ANALYSIS = "automated_analysis"


class DatasheetInformationCard(BaseModel):
    """Enhanced datasheet information card supporting blueprint sections and automation.
    
    This class represents a single section or subsection of a datasheet,
    containing both user-provided content and automated analysis results.
    """
    
    # Core identification
    section: DatasheetSection = Field(..., description="Main section this card belongs to")
    heading: str = Field(..., description="Main heading for this card")
    sub_heading: Optional[str] = Field(None, description="Optional sub-heading")
    
    # Content
    text: str = Field("", description="User-provided text content")
    card_type: CardType = Field(CardType.MANUAL, description="Type of card content")
    
    # Automated analysis results
    result_data: Optional[List[TabularStatistics]] = Field(
        None, 
        description="Automated statistical analysis results"
    )
    
    # Template integration
    template_questions: Optional[List[str]] = Field(
        None, 
        description="Original questions from the template"
    )
    
    # Metadata
    is_required: bool = Field(True, description="Whether this card is required for completeness")
    auto_populated: bool = Field(False, description="Whether content was automatically generated")
    
    # Additional structured data
    metadata: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Additional metadata for this card"
    )
    
    def is_complete(self) -> bool:
        """Check if this card has sufficient content.
        
        Returns:
            bool: True if the card has meaningful content.
        """
        if self.card_type == CardType.AUTOMATED:
            return self.result_data is not None and len(self.result_data) > 0
        elif self.card_type == CardType.MANUAL:
            return bool(self.text and self.text.strip() and 
                       not self.text.strip().startswith("[Please provide"))
        else:  # MIXED
            return (bool(self.text and self.text.strip()) or 
                   (self.result_data is not None and len(self.result_data) > 0))
    
    def to_markdown(self) -> str:
        """Convert this card to markdown format.
        
        Returns:
            str: Markdown representation of this card.
        """
        lines = []
        
        # Add heading
        if self.sub_heading:
            lines.append(f"### {self.sub_heading}")
        else:
            lines.append(f"### {self.heading}")
        lines.append("")
        
        # Add template questions if available
        if self.template_questions:
            for question in self.template_questions:
                lines.append(f"**{question}**")
                lines.append("")
        
        # Add user content
        if self.text:
            lines.append(self.text)
            lines.append("")
        
        # Add automated results
        if self.result_data:
            lines.append("#### Statistical Analysis")
            lines.append("")
            for stat in self.result_data:
                lines.append(f"**Column: {stat.column_name}**")
                lines.append(f"- Count: {stat.count}")
                if stat.mean_val is not None:
                    lines.append(f"- Mean: {stat.mean_val:.4f}")
                if stat.std_val is not None:
                    lines.append(f"- Standard Deviation: {stat.std_val:.4f}")
                if stat.min_val is not None:
                    lines.append(f"- Min: {stat.min_val}")
                if stat.max_val is not None:
                    lines.append(f"- Max: {stat.max_val}")
                if stat.lowest_quantile is not None:
                    lines.append(f"- 25th Percentile: {stat.lowest_quantile}")
                if stat.middle_quantile is not None:
                    lines.append(f"- Median: {stat.middle_quantile}")
                if stat.highest_quantile is not None:
                    lines.append(f"- 75th Percentile: {stat.highest_quantile}")
                lines.append("")
        
        return "\n".join(lines)
    
    @classmethod
    def create_from_template(cls, 
                           section: DatasheetSection,
                           heading: str,
                           sub_heading: Optional[str] = None,
                           questions: Optional[List[str]] = None) -> "DatasheetInformationCard":
        """Create a card from template information.
        
        Args:
            section: The datasheet section this card belongs to.
            heading: Main heading for the card.
            sub_heading: Optional sub-heading.
            questions: List of questions from the template.
            
        Returns:
            DatasheetInformationCard: New card instance.
        """
        return cls(
            section=section,
            heading=heading,
            sub_heading=sub_heading,
            text="[Please provide your answer here]",
            template_questions=questions or [],
            card_type=CardType.MANUAL,
            result_data=None,
            is_required=True,
            auto_populated=False
        )
    
    @classmethod
    def create_automated(cls,
                        section: DatasheetSection,
                        heading: str,
                        result_data: List[TabularStatistics],
                        description: str = "") -> "DatasheetInformationCard":
        """Create an automated analysis card.
        
        Args:
            section: The datasheet section this card belongs to.
            heading: Main heading for the card.
            result_data: Statistical analysis results.
            description: Optional description of the analysis.
            
        Returns:
            DatasheetInformationCard: New automated card instance.
        """
        return cls(
            section=section,
            heading=heading,
            sub_heading=None,
            text=description,
            result_data=result_data,
            card_type=CardType.AUTOMATED,
            template_questions=None,
            is_required=True,
            auto_populated=True
        )


class DatasheetStructure(BaseModel):
    """Complete datasheet structure containing multiple information cards.
    
    This class manages the overall organization and compilation of
    datasheet information cards into a complete document.
    """
    
    title: str = Field(..., description="Title of the datasheet")
    version: str = Field("1.0", description="Version of the datasheet")
    date_created: str = Field(..., description="Date when datasheet was created")
    
    cards: List[DatasheetInformationCard] = Field(
        default_factory=list,
        description="List of information cards comprising the datasheet"
    )
    
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata for the datasheet"
    )
    
    # Layout is not stored in the model but passed to methods that need it
    model_config = {"arbitrary_types_allowed": True}
    
    def add_card(self, card: DatasheetInformationCard) -> None:
        """Add an information card to the datasheet.
        
        Args:
            card: The information card to add.
        """
        self.cards.append(card)
    
    def get_cards_by_section(self, section: DatasheetSection) -> List[DatasheetInformationCard]:
        """Get all cards belonging to a specific section.
        
        Args:
            section: The section to filter by.
            
        Returns:
            List[DatasheetInformationCard]: Cards in the specified section.
        """
        return [card for card in self.cards if card.section == section]
    
    def is_complete(self) -> bool:
        """Check if the datasheet is complete.
        
        Returns:
            bool: True if all required cards are complete.
        """
        required_cards = [card for card in self.cards if card.is_required]
        return all(card.is_complete() for card in required_cards)
    
    def get_completion_status(self) -> Dict[str, Any]:
        """Get detailed completion status.
        
        Returns:
            Dict containing completion statistics.
        """
        total_cards = len(self.cards)
        completed_cards = sum(1 for card in self.cards if card.is_complete())
        required_cards = sum(1 for card in self.cards if card.is_required)
        completed_required = sum(1 for card in self.cards 
                               if card.is_required and card.is_complete())
        
        return {
            "total_cards": total_cards,
            "completed_cards": completed_cards,
            "completion_percentage": (completed_cards / total_cards * 100) if total_cards > 0 else 0,
            "required_cards": required_cards,
            "completed_required": completed_required,
            "required_completion_percentage": (completed_required / required_cards * 100) if required_cards > 0 else 0,
            "is_complete": self.is_complete()
        }
    
    def validate_against_layout(self, layout: "BaseLayout") -> Dict[str, Any]:
        """Validate this datasheet structure against a layout.
        
        Args:
            layout: The layout to validate against.
            
        Returns:
            Dict containing validation results.
        """
        # Get sections present in the datasheet
        present_sections = {card.section for card in self.cards}
        
        # Get required sections from layout
        required_sections = set(layout.required_sections)
        
        # Find missing required sections
        missing_required = required_sections - present_sections
        
        # Find extra sections (not in layout order)
        layout_sections = set(layout.get_ordered_sections())
        extra_sections = present_sections - layout_sections
        
        return {
            "is_valid": len(missing_required) == 0,
            "missing_required_sections": list(missing_required),
            "extra_sections": list(extra_sections),
            "present_sections": list(present_sections),
            "required_sections": list(required_sections)
        }
    
    def to_markdown(self, layout: Optional["BaseLayout"] = None) -> str:
        """Convert the entire datasheet to markdown format.
        
        Args:
            layout: Optional layout to define section ordering. If None, uses default ordering.
        
        Returns:
            str: Complete markdown representation of the datasheet.
        """
        lines = []
        
        # Header
        lines.extend([
            f"# {self.title}",
            "",
            f"**Version:** {self.version}",
            f"**Date:** {self.date_created}",
            "",
            "---",
            ""
        ])
        
        # Get section order from layout or use default
        if layout:
            sections_order = layout.get_ordered_sections()
        else:
            # Fallback to default ordering if no layout provided
            sections_order = [
                DatasheetSection.MOTIVATION,
                DatasheetSection.COMPOSITION,
                DatasheetSection.COLLECTION_PROCESS,
                DatasheetSection.PREPROCESSING,
                DatasheetSection.USES,
                DatasheetSection.DISTRIBUTION,
                DatasheetSection.MAINTENANCE,
                DatasheetSection.AUTOMATED_ANALYSIS
            ]
        
        for section in sections_order:
            section_cards = self.get_cards_by_section(section)
            if section_cards:
                # Section header
                section_title = section.value.replace('_', ' ').title()
                lines.extend([
                    f"## {section_title}",
                    ""
                ])
                
                # Add cards
                for card in section_cards:
                    lines.append(card.to_markdown())
                    lines.append("")
                
                lines.extend(["---", ""])
        
        return "\n".join(lines)
