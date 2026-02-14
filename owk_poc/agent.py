from typing import Any, Dict, List
import textwrap
from owk_poc.tools import get_targets, get_expressions, get_all_cancers

class Agent:
    """
    A minimal rule-based agent for processing cancer gene queries.
    
    This agent uses keyword matching to interpret natural language questions
    and retrieve relevant data from the underlying CSV dataset.
    """

    def process_query(self, query: str) -> str:
        """
        Processes a natural language query and returns a formatted response.
        """
        query = query.lower()
        
        # 1. Handle 'Help' Intent
        if any(k in query for k in ["help", "assist", "support"]):
            return self._get_help_message()

        # 2. Detect Cancer Types
        matched_cancers = self._detect_cancers(query)
        if not matched_cancers:
            return self._get_missing_context_message()

        # 3. Determine Action and Process
        is_expression_query = self._is_expression_query(query)
        response_sections = [
            self._process_cancer_entity(cancer, is_expression_query)
            for cancer in matched_cancers
        ]

        # 4. Build Final Response
        return self._assemble_response(response_sections, is_expression_query)

    def _detect_cancers(self, query: str) -> List[str]:
        """Identifies cancer types mentioned in the query."""
        all_available = get_all_cancers()
        return [c for c in all_available if c.lower() in query]

    def _is_expression_query(self, query: str) -> bool:
        """Determines if the user is asking for expression values."""
        return any(w in query for w in ["expression", "value", "median"])

    def _process_cancer_entity(self, cancer: str, is_expression: bool) -> str:
        """Retrieves and formats data for a single cancer type."""
        genes = get_targets(cancer)
        name = cancer.capitalize()

        if not genes:
            return f"**{name}**\nNo associated genes found in the dataset."
        
        if is_expression:
            data = get_expressions(genes)
            lines = "\n".join(f"- **{g}**: {v}" for g, v in data.items())
            return f"📊 **{name} Expression Values:**\n{lines}"
        
        gene_list_str = ", ".join(genes)
        return f"🧬 **{name} Genetic Targets:**\n{gene_list_str}"

    def _get_help_message(self) -> str:
        message = """
            👋 I'm here to help! You can ask me questions like:
            - 'What genes are involved in lung cancer?'
            - 'Show me expression values for breast cancer.'

            I can analyze data for several cancer types including lung, breast, and prostate.
        """
        return textwrap.dedent(message).strip()

    def _get_missing_context_message(self) -> str:
        options = ", ".join(get_all_cancers())
        message = f"""
            🔍 I don't have information on that specific cancer type in my dataset. 
            However, I can provide data for:

            **{options}**

            Please try asking about one of these.
        """
        return textwrap.dedent(message).strip()

    def _assemble_response(self, sections: List[str], is_expression: bool) -> str:
        intro = "Based on the analysis of the dataset, here is the requested information for the identified cancer types:"
        
        footer = (
            "💡 These values represent the central tendency of gene expression levels in the cohort."
            if is_expression else 
            "💡 These values represent the gene targets for the identified cancer type."
        )
        
        body = "\n\n---\n\n".join(sections)
        return f"{intro}\n\n{body}\n\n{footer}"

if __name__ == "__main__":
    agent = Agent()
    print(agent.process_query("What genes are involved in lung cancer?"))
