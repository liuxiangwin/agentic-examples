package org.acme;

import org.eclipse.microprofile.rest.client.inject.RestClient;

import dev.langchain4j.agent.tool.Tool;
import io.quarkus.logging.Log;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;

@ApplicationScoped
public class SearchService {

    @Inject
    @RestClient
    SearchClient searchClient;

    public String search(String query) {
        Log.info("Search query: " + query);
        return searchClient.search(query);
    }
} 
