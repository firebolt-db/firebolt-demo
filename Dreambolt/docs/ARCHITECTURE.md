# 🏗️ DreamBolt Architecture Overview

**Last Updated:** 2025-06-20  
**Version:** v0.1 MVP + Future Roadmap  
**Status:** ✅ Core pipeline functional

## 📊 High-Level Architecture

```mermaid
flowchart TB
    %% Current Implementation (Solid Boxes)
    subgraph "Data Input Layer"
        A[Local Files<br/>CSV/Parquet] 
        B[S3 URIs]:::disabled
        C[Configuration<br/>env.template]
    end
    
    subgraph "CLI Interface"
        D[Main CLI<br/>cli.py - Typer]:::partial
        E[Working CLI<br/>cli_working.py - argparse]
        F[__main__.py<br/>Module Entry]
    end
    
    subgraph "Core Processing Engine"
        G[Data Ingestion<br/>ingest.py / ingest_simple.py]
        H[Schema Analysis<br/>SchemaInfo]
        I[Data Cleaning<br/>Column Standardization]
        J[LLM Synthesis<br/>synth.py / synth_simple.py]
        K[Embedding Generation<br/>Vector Embeddings]
    end
    
    subgraph "LLM Integration"
        L[OpenAI API<br/>GPT Models]
        M[DataDreamer<br/>Processing Framework]:::partial
        N[HuggingFace<br/>Local Models]:::planned
    end
    
    subgraph "Data Output Layer"
        O[Parquet Files<br/>Optimized Storage]
        P[Firebolt Database<br/>firebolt_io.py]
        Q[Table Creation<br/>Dynamic Schema]
        R[Data Loading<br/>COPY Operations]
    end
    
    subgraph "Quality & Testing"
        S[Test Suite<br/>pytest]:::partial
        T[Coverage Reports<br/>pytest-cov]
        U[Integration Tests<br/>CLI Testing]:::partial
    end
    
    %% Planned Features (Dashed Boxes)
    subgraph "Planned: Advanced Input"
        V[JSON/XML Support]:::planned
        W[Excel Files]:::planned
        X[Streaming Data]:::planned
        Y[Custom Transformations]:::planned
    end
    
    subgraph "Planned: Enterprise Features"
        Z[Web UI Dashboard]:::planned
        AA[Multi-tenant Support]:::planned
        BB[Data Lineage Tracking]:::planned
        CC[Scheduling & Orchestration]:::planned
        DD[Audit Logging]:::planned
    end
    
    subgraph "Planned: Advanced AI"
        EE[Multi-LLM Providers]:::planned
        FF[Custom Prompt Library]:::planned
        GG[Semantic Similarity]:::planned
        HH[Auto Data Profiling]:::planned
        II[Quality Scoring]:::planned
    end
    
    subgraph "Planned: Developer Experience"
        JJ[Interactive Wizard]:::planned
        KK[Plugin Architecture]:::planned
        LL[Performance Profiling]:::planned
        MM[Auto-Documentation]:::planned
        NN[CI/CD Pipeline]:::planned
    end
    
    %% Current Data Flow
    A --> G
    B -.-> G
    C --> D
    C --> E
    D -.-> G
    E --> G
    F --> D
    F --> E
    
    G --> H
    H --> I
    I --> J
    J --> K
    
    J --> L
    J --> M
    
    G --> O
    K --> O
    O --> P
    P --> Q
    Q --> R
    
    %% Testing Integration
    E --> S
    G --> S
    S --> T
    
    %% Planned Integrations
    V -.-> G
    W -.-> G
    X -.-> G
    Y -.-> I
    
    J -.-> EE
    J -.-> FF
    K -.-> GG
    I -.-> HH
    H -.-> II
    
    P -.-> Z
    R -.-> BB
    S -.-> NN
    
    E -.-> JJ
    G -.-> KK
    J -.-> LL
    T -.-> MM
    
    %% Styling
    classDef planned stroke-dasharray: 5 5, fill:#e1f5fe
    classDef partial stroke-dasharray: 3 3, fill:#fff3e0
    classDef disabled stroke-dasharray: 8 8, fill:#ffebee, color:#666
```

## 🔍 Component Status Legend

| Symbol | Status | Description |
|--------|--------|-------------|
| **Solid** | ✅ Implemented | Fully functional and tested |
| **Dashed** | 🚧 Planned | In roadmap, not yet implemented |
| **Dot-dash** | ⚡ Partial | Partially implemented or has limitations |
| **Long-dash** | ❌ Disabled | Temporarily disabled or broken |

## 📋 Current Architecture Details

### ✅ **Implemented Components**

#### **Data Input Layer**
- **Local Files**: Full CSV/Parquet support with schema inference
- **Configuration**: Environment template with credential management

#### **CLI Interface** 
- **Working CLI** (`cli_working.py`): Argparse-based, fully functional
- **Module Entry** (`__main__.py`): Python module execution support

#### **Core Processing Engine**
- **Data Ingestion**: Multi-format loading with simplified fallbacks
- **Schema Analysis**: Automatic type detection and categorical inference  
- **Data Cleaning**: Column standardization and optimization
- **Parquet Output**: Optimized storage with embedding support

#### **Database Integration**
- **Firebolt Connection**: Engine management and table operations
- **Dynamic Schema**: Auto-generated CREATE TABLE statements
- **Data Loading**: Bulk COPY operations and fallback INSERT

### ⚡ **Partially Implemented**

#### **CLI Interface**
- **Main CLI** (`cli.py`): Typer-based but has Python 3.13 compatibility issues
- **Rich UI**: Progress bars working, but limited by typer issues

#### **LLM Integration**
- **LLM Synthesis**: Statistical fallback when DataDreamer unavailable
- **DataDreamer**: Manual installation required, not in requirements.txt

#### **Testing Framework**
- **Test Suite**: Structure exists but most tests skipped with TODOs
- **Integration Tests**: CLI testing framework setup but needs implementation

### ❌ **Currently Disabled**

#### **S3 Integration**
- **S3 URIs**: Temporarily disabled due to dependency issues
- **Reason**: boto3/s3fs import conflicts in simplified modules

## 🚀 **Planned Features Roadmap**

### **Phase 1: Foundation Completion**
- ✅ Core ingestion pipeline (DONE)
- 🚧 Complete test suite implementation
- 🚧 Fix typer/Python 3.13 compatibility
- 🚧 Re-enable S3 support with proper error handling

### **Phase 2: Advanced Data Processing**
- 🚧 JSON/XML/Excel format support
- 🚧 Streaming ingestion for large datasets  
- 🚧 Custom transformation pipelines
- 🚧 Data quality scoring and alerts

### **Phase 3: Enterprise Features**
- 🚧 Web UI dashboard for pipeline monitoring
- 🚧 Multi-tenant data isolation
- 🚧 Data lineage tracking
- 🚧 Scheduling and orchestration
- 🚧 Audit logging and compliance

### **Phase 4: Advanced AI & ML**
- 🚧 Multi-LLM provider support (Anthropic, local models)
- 🚧 Advanced prompt template library
- 🚧 Semantic similarity matching
- 🚧 Automated data profiling and insights
- 🚧 Custom embedding models

### **Phase 5: Developer Experience**
- 🚧 Interactive CLI wizard mode
- 🚧 Plugin architecture for custom steps
- 🚧 Performance profiling tools
- 🚧 Auto-documentation generation
- 🚧 Complete CI/CD pipeline

## 🔄 Data Flow Architecture

### **Current Pipeline**
1. **Input** → Local CSV/Parquet files
2. **Ingestion** → Schema analysis and data loading
3. **Processing** → Column cleaning and type optimization
4. **Synthesis** → Optional LLM-generated rows (fallback mode)
5. **Embeddings** → Optional vector generation for search
6. **Output** → Parquet files with standardized schema
7. **Loading** → Firebolt table creation and data copy

### **Error Handling Strategy**
- **Graceful Degradation**: Fallback modes when external services unavailable
- **Simulation Mode**: Mock operations for development/testing
- **Clear Messaging**: User-friendly error messages with troubleshooting steps

### **Configuration Management**
- **Environment Variables**: Centralized credential management
- **Template System**: `env.template` for easy setup
- **Validation**: Runtime checks for required configurations

## 🛠️ Technical Architecture Decisions

### **Module Design Principles**
- **<200 LOC per file**: Maintainable, focused modules
- **Simplified Fallbacks**: `*_simple.py` versions bypass complex dependencies
- **Rich Documentation**: Comprehensive docstrings and type hints
- **Smoke Tests**: Built-in testing with `if __name__ == "__main__"`

### **Dependency Strategy**
- **Core Dependencies**: pandas, pyarrow for data processing
- **Optional Dependencies**: Graceful handling of missing LLM/cloud libraries
- **Version Pinning**: Upper bounds for stability, lower bounds for features

### **Testing Philosophy**
- **Integration-First**: Test real workflows over unit tests
- **CLI Testing**: End-to-end command validation
- **Mock External APIs**: Avoid API costs in CI/CD

## 🔧 Development Workflow

### **Vibe-Coding Principles**
1. **Plan** → Update PLAN.md with feature
2. **Test** → Write failing tests first  
3. **Code** → Implement until tests pass
4. **Commit** → Atomic commits with clear messages

### **Quality Gates**
- **File Size**: Maximum 200 LOC per module
- **Test Coverage**: Integration tests for all major workflows
- **Documentation**: Self-documenting code with examples

---

*This architecture evolves with the codebase. Last synchronized: Repository audit and CLI fixes completed.* 