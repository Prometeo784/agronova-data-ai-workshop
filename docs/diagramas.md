# Diagramas

GitHub renderiza estos bloques Mermaid directamente.

## 1. Plataforma con Medallion y gobernanza transversal

```mermaid
flowchart LR
    subgraph FUENTES["Fuentes"]
        ERP["ERP (SQL)"]
        XL["Excel de calidad"]
        API["API logística"]
        MA["Maestros"]
    end
    ING["Ingesta incremental batch"]
    BR["Bronze: copia fiel"]
    SI["Silver: validado"]
    CU["Cuarentena"]
    GO["Gold: modelo para consumo"]
    BI["BI y scorecards"]
    ML["Modelo de riesgo"]
    RG["RAG documental"]
    GOB["Gobernanza transversal: catálogo, linaje, permisos, calidad, monitoreo"]
    ERP --> ING
    XL --> ING
    API --> ING
    MA --> ING
    ING --> BR --> SI --> GO
    SI --> CU
    GO --> BI
    GO --> ML
    GO --> RG
    GOB -.-> ING
    GOB -.-> BR
    GOB -.-> SI
    GOB -.-> GO
```

## 2. Flujo RAG: el filtro de permisos va antes del contexto

```mermaid
flowchart LR
    subgraph PREP["Preparación, antes de consultar"]
        D["Documentos vigentes"] --> C["Chunking y limpieza"] --> M["Metadatos y permisos"] --> I["Índice (embeddings)"]
    end
    subgraph CONS["Consulta, en línea"]
        P["Pregunta con identidad"] --> R["Recuperación + filtro de permisos"] --> X["Contexto autorizado"] --> A["Respuesta con citas o abstención"]
    end
    I -.-> R
    EV["Evaluación y monitoreo"] -.-> A
```

## 3. Pipeline verde, dato incorrecto: reconciliación y umbral

```mermaid
flowchart LR
    B["Bronze: 1,000"] --> S["Silver: 938"]
    B --> Q["Cuarentena: 62"]
    S --> RC["Reconciliación: 1,000 = 938 + 62"]
    Q --> AL["Alerta: 6.2 % supera el umbral de 1 %"]
```
