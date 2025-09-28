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

            rag_service_comp -->|"Sends prompts to"| llm_service_comp
            rag_service_comp -->|"Retrieves/Stores embeddings from"| vector_store_service_comp
            rag_service_comp -->|"Stores/Retrieves document metadata from"| app_db_comp

            %% вместо services_container → config делаем связи от компонентов
            rag_service_comp -->|"Uses configuration from"| app_config_comp
            llm_service_comp -->|"Uses configuration from"| app_config_comp
            vector_store_service_comp -->|"Uses configuration from"| app_config_comp
        end

        document_routes -->|"Triggers document processing in"| rag_service_comp
        query_routes -->|"Requests query processing from"| rag_service_comp
        api_container -->|"Uses configuration from"| app_config_comp
    end

    user -->|"Uploads/Manages documents via"| document_routes
    user -->|"Submits queries via"| query_routes

    llm_service_comp -->|"Communicates with | API"| llm_service_ext
    vector_store_service_comp -->|"Communicates with | API"| vector_db_ext
