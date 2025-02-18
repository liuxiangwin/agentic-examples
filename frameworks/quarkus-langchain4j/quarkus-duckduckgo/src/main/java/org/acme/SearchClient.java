package org.acme;

import org.eclipse.microprofile.rest.client.inject.RegisterRestClient;

import dev.langchain4j.agent.tool.Tool;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.core.MediaType;

@ApplicationScoped
@RegisterRestClient(configKey = "duckduckgo")
public interface SearchClient {

  @GET
  @Path("/q={query}&format=json")
  @Consumes(MediaType.APPLICATION_JSON)
  @Tool("Perform internet searches using duckduckgo")
  String search(String query); 
}

