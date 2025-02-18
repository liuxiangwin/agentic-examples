package org.acme;


import io.quarkus.picocli.runtime.annotations.TopCommand;
import jakarta.inject.Inject;
import picocli.CommandLine.Command;
import picocli.CommandLine.Parameters;

@TopCommand
@Command(name = "search", mixinStandardHelpOptions = true)
public class SearchCommand implements Runnable {

    @Parameters(index="0", description = "Your query.")
    String query;

    @Inject
    AiService searchService;

    @Override
    public void run() {
        System.out.printf("Search result: %s\n", searchService.search(query));
    }

}
