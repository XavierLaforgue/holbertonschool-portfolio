# Diagrams

All technical diagrams for the `animize_eat` project.

## Production Architecture

```mermaid
flowchart TD
    Browser["Browser"]

    Browser -->|"all traffic"| Nginx

    subgraph docker["Docker Compose"]
        Nginx["Nginx :80"]

        Nginx -->|"/api/ & /admin/"| backend1 & backend2 & backendN

        subgraph backend_pool["back-end (gunicorn)"]
            backend1["replica 1"]
            backend2["replica 2"]
            backendN["replica N"]
        end
        
        backend1 & backend2 & backendN --> DB

        DB[("PostgreSQL 18")]
        
        DB --- pg_vol

        pg_vol[/"postgres_data"/]

        Nginx -->|"/ (SPA)"| frontend_vol

        frontend_vol[/"frontend_build"/]

        Nginx -->|"/static/"| static_vol

        static_vol[/"backend_static"/]

        Nginx -->|"/media/"| media_vol

        media_vol[/"backend_media"/]
    end
```
