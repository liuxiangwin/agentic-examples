package org.acme;

import io.quarkiverse.langchain4j.RegisterAiService;
import io.quarkiverse.langchain4j.ToolBox;
import jakarta.enterprise.context.ApplicationScoped;

@RegisterAiService
@ApplicationScoped
public interface AiService {
    
    @ToolBox(SearchClient.class)
    String search(String query);
}

