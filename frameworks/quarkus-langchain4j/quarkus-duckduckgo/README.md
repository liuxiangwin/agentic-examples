# Quarkus DuckDuckGo

This is a simple Quarkus CLI application that performs a DuckDuckGo searches.
The actual search and the output of the CLI is taken care by the LLM, 
while the actual search is done by the DuckDuckGo API with using the Quarkus REST client.
The client is used by the LLM as a tool / function.

## Supported models

The example has been tested with the following models on OpenShift AI:
- Grantie 3
- Mistral 7

The actual model configuration has been externalized using the following environment variables:

- LLM_MODEL_URL
- LLM_MODEL_NAME
- LLM_API_KEY


## Building the application

The application can be built both in JVM and Native modes.

### JVM mode

```bash
./mvnw package
```
It can then be run using:

```bash
java -jar target/quarkus-app/quarkus-run.jar "When was Quarkus first released?"
```

### Native mode

```bash
./mvnw package -Pnative
```
It can then be run using:

```bash
./target/quarkus-app/quarkus-run "When was Quarkus first released?"
```
