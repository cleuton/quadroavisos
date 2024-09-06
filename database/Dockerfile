# Use the official PostgreSQL image from the Docker Hub
FROM postgres:latest

# Set environment variables for PostgreSQL
ENV POSTGRES_DB=backend_db
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=password

# Copy the SQL script to the Docker image
COPY ./create.sql /docker-entrypoint-initdb.d/

# Expose the PostgreSQL port
EXPOSE 5432