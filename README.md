```mermaid
graph TD

    user["User<br>[External]"]
    llm_service_ext["LLM Service<br>/app/services/llm_service.py"]
    vector_db_ext["Vector Database<br>/app/services/vectorstore.py"]
    subgraph ai_doc_agent["AI Doc Agent<br>/app"]
        subgraph api_container["API<br>/app/api"]
            document_routes["Document Routes<br>/app/api/routes_documents.py"]
            query_routes["Query Routes<br>/app/api/routes_query.py"]
        end
        subgraph services_container["Services<br>/app/services"]
            llm_service_comp["LLM Service Component<br>/app/services/llm_service.py"]
            rag_service_comp["RAG Service<br>/app/services/rag_service.py"]
            vector_store_service_comp["Vector Store Service<br>/app/services/vectorstore.py"]
            app_db_comp["Application Database Component<br>/app/core/db.py"]
            app_config_comp["Application Configuration<br>/app/core/config.py"]
            %% Edges at this level (grouped by source)
            rag_service_comp["RAG Service<br>/app/services/rag_service.py"] -->|"Sends prompts to"| llm_service_comp["LLM Service Component<br>/app/services/llm_service.py"]
            rag_service_comp["RAG Service<br>/app/services/rag_service.py"] -->|"Retrieves/Stores embeddings from"| vector_store_service_comp["Vector Store Service<br>/app/services/vectorstore.py"]
            rag_service_comp["RAG Service<br>/app/services/rag_service.py"] -->|"Stores/Retrieves document metadata from"| app_db_comp["Application Database Component<br>/app/core/db.py"]
            services_container["Services<br>/app/services"] -->|"Uses configuration from"| app_config_comp["Application Configuration<br>/app/core/config.py"]
        end
        %% Edges at this level (grouped by source)
        document_routes["Document Routes<br>/app/api/routes_documents.py"] -->|"Triggers document processing in"| rag_service_comp["RAG Service<br>/app/services/rag_service.py"]
        query_routes["Query Routes<br>/app/api/routes_query.py"] -->|"Requests query processing from"| rag_service_comp["RAG Service<br>/app/services/rag_service.py"]
        api_container["API<br>/app/api"] -->|"Uses configuration from"| app_config_comp["Application Configuration<br>/app/core/config.py"]
    end
    %% Edges at this level (grouped by source)
    user["User<br>[External]"] -->|"Uploads/Manages documents via"| document_routes["Document Routes<br>/app/api/routes_documents.py"]
    user["User<br>[External]"] -->|"Submits queries via"| query_routes["Query Routes<br>/app/api/routes_query.py"]
    llm_service_comp["LLM Service Component<br>/app/services/llm_service.py"] -->|"Communicates with | API"| llm_service_ext["LLM Service<br>/app/services/llm_service.py"]
    vector_store_service_comp["Vector Store Service<br>/app/services/vectorstore.py"] -->|"Communicates with | API"| vector_db_ext["Vector Database<br>/app/services/vectorstore.py"]

```
