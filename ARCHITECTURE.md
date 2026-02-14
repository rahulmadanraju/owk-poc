# Agentic POC - Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    USER (Non-Technical Stakeholder)         │
│                    "What genes are in lung cancer?"         │
└────────────────────────────┬────────────────────────────────┘
                             │ Natural Language Query
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                  PRESENTATION LAYER                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Streamlit Web Interface (app.py)                     │  │
│  │  - Chat UI                                            │  │
│  │  - Session state management                           │  │
│  │  - Display results                                    │  │
│  └───────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────┘
                             │ process_query(query)
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    AGENT LAYER                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Agent (agent.py)                                     │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  Intent Classifier(Keyword-based)               │  │  │
│  │  │  - Dynamic cancer name scanning(Multi-entity)   │  │  │
│  │  │  - Help query detection                         │  │  │
│  │  │  - Gene targets query detection                 │  │  │
│  │  │  - Expression values query detection            │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└──────────────┬─────────────────────────┬────────────────────┘
               │                         │
               │ get_targets(cancer)     │ get_expressions(genes)
               ▼                         ▼
┌──────────────────────────┐  ┌──────────────────────────────┐
│   FUNCTION LAYER         │  │   FUNCTION LAYER             │
│  ┌────────────────────┐  │  │  ┌────────────────────────┐  │
│  │ get_targets()      │  │  │  │ get_expressions()      │  │
│  │ Returns: List[str] │  │  │  │ Returns:Dict[str,float]│  │
│  └────────────────────┘  │  │  └────────────────────────┘  │
└──────────┬───────────────┘  └───────────┬──────────────────┘
           │                              │
           │ Filter by cancer_indication  │ Filter by gene list
           ▼                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATA LAYER                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Data Tools (tools.py)                                │  │
│  │  - pandas DataFrame operations                        │  │
│  │  - Case-insensitive matching                          │  │
│  │  - Error handling                                     │  │
│  └───────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────┘
                             │ pd.read_csv()
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                   DATA SOURCE                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  data.csv                                             │  │
│  │  Columns: cancer_indication, gene, median_value       │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. **Presentation Layer** (app.py)
- **Technology**: Streamlit
- **Responsibility**: User interface, chat management
- **Input**: Natural language text
- **Output**: Formatted responses

### 2. **Agent Layer** (agent.py)
- **Technology**: Python (Keyword Matching)
- **Responsibility**: Dynamic intent classification, query routing, multi-entity orchestration
- **Logic**:
  - Scanning against `get_all_cancers()` list (supports multiple matches)
  - `"help"` / `"assist"` → Return help text
  - `"expression"` / `"median"` / `"value"` → Analysis intent
  - **Stratified Output**: Groups results by cancer type if multiple entities are found.
### 3. **Function Layer** (tools.py functions)
- **get_targets(cancer_name)**
  - Input: Cancer type (string)
  - Output: List of gene names
  - Logic: Filter DataFrame by cancer_indication

- **get_expressions(genes)**
  - Input: List of gene names
  - Output: Dictionary {gene: median_value}
  - Logic: Filter DataFrame by gene list

### 4. **Data Layer** (tools.py)
- **Technology**: pandas
- **Responsibility**: CSV loading, data filtering
- **Features**: Error handling, case-insensitive matching

### 5. **Data Source**
- **Format**: CSV file
- **Location**: `data/data.csv`
- **Schema**: cancer_indication, gene, median_value

## Data Flow Example

```
User Query: "What are the main genes involved in lung cancer?"
    ↓
Streamlit captures input
    ↓
agent.process_query("What are the main genes involved in lung cancer?")
    ↓
Scans available cancers: "lung" found in query string
    ↓
Extracts: matched_cancer = "lung"
    ↓
Calls: get_targets("lung")
    ↓
DataFrame filter: df[df['cancer_indication'] == 'lung']['gene']
    ↓
Returns: ['ALK', 'RET', 'ROS1', 'STK11', 'KRAS']
    ↓
Agent formats response
    ↓
Streamlit displays: "The key genetic targets associated with lung cancer are: ALK, RET, ROS1, STK11, KRAS"
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Container                     │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Python 3.10 Runtime                              │  │
│  │  ├── Streamlit Server (Port 8501)                 │  │
│  │  ├── owk_poc/ (Application code)                  │  │
│  │  └── data/ (CSV file)                             │  │
│  └───────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────┘
                             │ Port 8501
                             ▼
                    ┌─────────────────┐
                    │  User's Browser │
                    │  localhost:8501 │
                    └─────────────────┘
```
