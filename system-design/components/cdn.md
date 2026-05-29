# Content Delivery Networks (CDNs)

CDNs use geographically distributed edge servers to cache content closer to users.

## How it Works
- User request → DNS resolves to nearest edge → Cache hit/miss → Serve content

## Benefits
- Reduced latency
- Bandwidth savings
- Origin protection

## Trade-offs and Considerations
- CDNs reduce latency and bandwidth but add cost and complexity.
- Cache invalidation and consistency are operational challenges.

## Architecture Diagram
```mermaid
graph TD
    User[User] -->|GET logo.png| Anycast[Anycast IP]

    Anycast --> EdgeProxy

    subgraph Edge[Edge CDN]
        EdgeProxy[Edge Proxy]

        subgraph EdgePool[Node Pool]
            EdgeIndex[Cache Index]
            EdgeSSD[SSD]
        end

        EdgeProxy -->|Consistent Hash Lookup| EdgeIndex
        EdgeIndex --> EdgeSSD
    end

    EdgeProxy -->|Edge Miss| RegionalProxy

    subgraph Regional[Regional / Tiered Cache]
        RegionalProxy[Regional Proxy]

        subgraph RegionalPool[Node Pool]
            RegionalIndex[Cache Index]
            RegionalSSD[SSD]
        end

        RegionalProxy -->|Consistent Hash Lookup| RegionalIndex
        RegionalIndex --> RegionalSSD
    end

    RegionalProxy -->|Regional Miss| Reserve[Reserved Object Storage]
    Reserve -->|Reserve Miss| Origin[Origin]
```
