# Infrastructure Orchestration

This document covers orchestration platforms for containerized and distributed systems, focusing on Kubernetes and Borg. It emphasizes scheduling, scaling, reliability, and design trade-offs relevant to system design interviews.

## Components

### Kubernetes

Kubernetes (K8s) is an open-source container orchestration system derived from Google’s internal Borg and Omega systems. It automates deployment, scaling, and management of containerized applications.

#### *Core Concepts*

- **Cluster**: Set of worker nodes managed by a control plane.
- **Pod**: Smallest deployable unit (1+ containers with shared network/storage).
- **Deployment / ReplicaSet**: Declarative state management; scaling and rollouts.
- **Service**: Stable network abstraction; load balances Pods.
- **ConfigMap / Secret**: Externalized configuration and sensitive values.
- **Namespaces**: Resource and policy isolation within a cluster.
- **Scheduler**: Places Pods on nodes based on resource requests, affinity/anti-affinity, taints/tolerations, and priorities.

##### ConfigMap

ConfigMaps are Kubernetes objects used to externalize configuration data from container images, allowing configuration to be decoupled from application code. They store non-sensitive configuration as key-value pairs or configuration files, which Pods can consume as environment variables, command-line arguments, or mounted files.

**Trade-offs:** Using ConfigMaps allows for dynamic configuration changes without rebuilding container images, improving flexibility. However, ConfigMaps are not designed for sensitive data; Secrets should be used instead for credentials or private information. Also, ConfigMaps are eventually consistent and may cause transient inconsistencies if updated rapidly.

**When to use Secrets instead:** If configuration data contains sensitive information such as passwords, tokens, or keys, use Secrets which are stored in a base64-encoded form and can be integrated with external secret management systems.

**Interview prompt:** How would you design configuration management to enable safe updates and rollbacks in a Kubernetes environment?

##### CRDs (Custom Resource Definitions)

CRDs extend the Kubernetes API by allowing users to define their own resource types. This enables custom controllers and Operators to manage application-specific resources declaratively, following the Kubernetes reconciliation model.

Operators built on CRDs automate complex application lifecycle tasks such as backups, upgrades, and scaling by embedding domain knowledge into controllers.

**Use cases:** Managing databases, message queues, or other stateful services with custom logic beyond built-in Kubernetes objects.

**Interview prompt:** How do CRDs and Operators enable Kubernetes extensibility, and what challenges arise in building reliable custom controllers?

##### Controllers

Controllers are control loops that continuously monitor the cluster state and reconcile it toward the desired state defined by Kubernetes objects. For example, the ReplicaSetController ensures the specified number of pod replicas are running, and the JobController manages batch job execution.

The reconciliation model is fundamental to Kubernetes' self-healing capabilities: controllers detect divergence from desired state and take corrective actions automatically.

**Interview prompt:** Why is the reconciliation loop model critical for distributed system reliability, and how does it affect system design?

##### Stateless vs Stateful

Stateless services do not persist client session information between requests; each request is independent. Stateful services persist session information, storage, or connections across requests, requiring mechanisms for data durability and consistency.

**Is this the same as "client session information between requests"?** Yes, but statefulness also broadly includes persistent storage and long-lived connections beyond just client sessions.

**Interview prompt:** How would you design a stateful application on Kubernetes, and what challenges arise compared to stateless services?

##### RBAC (Role-Based Access Control)

Kubernetes enforces fine-grained permissions using RBAC, which defines Roles and ClusterRoles specifying allowed actions on resources, and RoleBindings or ClusterRoleBindings that assign these roles to users or service accounts.

RBAC is critical for multi-tenancy and security, enabling isolation of privileges and minimizing blast radius of compromised components.

**Interview prompt:** How would you design RBAC policies to balance security and operational flexibility in a multi-tenant cluster?

##### Service Discovery

Kubernetes provides service discovery primarily through Services, which create stable IPs and DNS names for groups of Pods. kube-proxy manages network rules to route traffic to healthy Pod endpoints, and DNS resolves service names within the cluster.

In contrast, Borg used internal naming systems tightly integrated with Google's infrastructure for service discovery.

**Interview prompt:** How does Kubernetes service discovery enable scaling and resilience, and what are the trade-offs compared to internal naming systems like Borg’s?

##### Isolation of Networking

Kubernetes uses Namespaces to provide logical isolation of resources and policies. NetworkPolicies define fine-grained rules controlling traffic between Pods and external endpoints. CNI (Container Network Interface) plugins implement networking layers that enable flexible, pluggable network configurations.

Isolation helps secure multi-tenant environments and limit blast radius of failures, but adds complexity and potential performance overhead.

**Interview prompt:** How would you design network isolation in Kubernetes to support secure multi-tenancy without sacrificing performance?

#### *Strengths*
- Declarative, portable, cloud-agnostic.
- Horizontal autoscaling (Pods) and cluster autoscaling (nodes).
- Rolling updates, canaries, and self-healing (Pod rescheduling).
- Extensibility via CRDs, Operators, and pluggable controllers.

#### *Trade-offs*
- Operational complexity; steep learning curve.
- Scheduling is less tightly optimized for extreme scale than Borg.
- Network abstraction layers (CNI, Ingress) add complexity.
- State management (e.g., persistent storage) requires careful design.

#### *Patterns*
- Stateless services → Deployments + Services.
- Stateful workloads → StatefulSets + PersistentVolumes.
- Event-driven or batch jobs → Jobs/CronJobs.
- Multi-tenancy via Namespaces + RBAC.

#### *Pitfalls*
- Over-abstracting: not all workloads need Kubernetes.
- Misconfigured resource requests → wasted capacity or instability.
- Poor observability/logging → hidden scaling/failure issues.
- Ignoring pod disruption budgets → cascading downtime during upgrades.

#### *Interview Q&A*

**Q1. How would you design for service discovery, scaling, and updates in Kubernetes?**  
A: Use Kubernetes Services to provide stable endpoints and internal DNS for service discovery. kube-proxy manages routing to healthy Pods. For scaling, leverage Horizontal Pod Autoscaler (HPA) for Pods and Cluster Autoscaler for nodes. Rolling updates and rollbacks are managed via Deployments, enabling zero-downtime upgrades.

**Q2. How do you ensure multi-tenancy fairness and isolation?**  
A: Use Namespaces to logically separate resources and workloads. Enforce resource quotas and limits per namespace to ensure fairness. Apply RBAC to restrict access and privileges. Use NetworkPolicies to isolate network traffic between tenants.

**Q3. What’s your approach to stateful workloads?**  
A: Deploy StatefulSets for stateful applications, which provide stable identities and persistent storage. Use PersistentVolumes and StorageClasses to provision storage that survives Pod restarts and rescheduling.

**Q4. How does Kubernetes balance flexibility vs operational complexity?**  
A: Kubernetes offers extensibility through CRDs, Operators, and pluggable controllers, allowing custom resources and automation. This flexibility increases operational complexity, requiring careful management of custom components and APIs.

---

### Borg

Borg is Google’s internal cluster manager and container orchestration system, precursor to Kubernetes. It emphasizes efficiency, priority scheduling, and scale across massive clusters.

#### *Core Concepts*
- **Job / Task Model**: A job is composed of many identical tasks scheduled across nodes.
- **Cells**: Borg clusters (cells) isolate workloads at massive scale.
- **Priorities & Quotas**: High-priority production jobs can preempt lower-priority batch jobs; quotas ensure fairness across teams.
- **Bin Packing**: Aggressively co-locates workloads to maximize utilization.
- **Failure Recovery**: Tasks automatically rescheduled on node failures.

#### *Colossus*

Colossus is Google's distributed storage system that underpins Borg's persistent storage needs. It provides high durability, availability, and scalability by distributing data across multiple machines and datacenters.

Borg integrates tightly with Colossus to ensure that stateful workloads have reliable storage, enabling recovery and replication transparently.

**Interview relevance:** Understanding Colossus helps in designing storage-aware scheduling and failure recovery strategies in large-scale cluster management.

#### *Strengths*
- Extremely high utilization of resources.
- Transparent failure recovery; robust preemption model.
- Designed for 100k+ tasks and 10k+ nodes.
- Seamless coexistence of batch and production jobs.

#### *Trade-offs*
- Centralized monolithic scheduler: highly optimized but less flexible.
- Built for Google’s environment only (not portable).
- Tight integration with internal systems (Colossus, Spanner, monitoring).

#### *Comparison with Kubernetes*
| Aspect | Borg | Kubernetes |
|--------|------|------------|
| Target | Google-only | Open source, portable |
| Scheduler | Monolithic, optimized | Modular, pluggable |
| Scale | 10k+ nodes, 100k+ tasks | Hundreds–thousands nodes |
| Priority/Preemption | Core design principle | Available, less quota-integrated |
| Utilization | Extremely high | Good but more general-purpose |
| Storage | Colossus + internal systems | CSI plugins, cloud volumes |

#### *Interview Q&A*

**Q1. How does Borg schedule jobs? How does it differ from Kubernetes?**  
Borg uses a centralized, monolithic scheduler optimized for bin-packing and fairness at Google scale. Kubernetes uses a pluggable scheduler, favoring flexibility and portability over hyper-optimized scale.

**Q2. How does Borg handle quotas, priorities, and preemption?**  
Borg enforces team quotas and uses strict job priorities. High-priority prod jobs preempt lower-priority batch jobs, which are resumed later. Kubernetes supports PriorityClasses and Pod preemption but is less integrated with quota fairness.

**Q3. What changes when scheduling 100k tasks vs 1k tasks?**  
At 100k scale, scheduler latency, bin-packing efficiency, and continuous hardware failure recovery become dominant challenges. Small inefficiencies multiply drastically, requiring global optimization.

**Q4. What happens when a node fails in Borg?**  
Borg detects failures quickly, reschedules tasks on healthy nodes, and provides near-seamless recovery for replicated prod jobs. Batch jobs are resumed without manual intervention.

**Q5. Why might Borg centralize scheduling while Kubernetes allows modular plugins?**  
Borg is optimized for Google’s internal environment — centralization provides efficiency and consistency. Kubernetes targets diverse environments, so modularity enables flexibility for different infrastructure and workloads.

#### *Interview Q&A*

**Q1. How would you design a scheduler for fairness and utilization at scale?**  
A: Implement a centralized scheduler that uses bin-packing algorithms to maximize resource utilization and enforces quotas to ensure fairness across teams and workloads.

**Q2. When is preemption useful and what are the trade-offs?**  
A: Preemption allows high-priority jobs to take resources from lower-priority ones, ensuring critical workloads meet SLAs. The trade-off is potential disruption and increased latency for preempted jobs.

**Q3. How do you handle mixed production and batch workloads in one cluster?**  
A: Assign higher priorities to production jobs so they preempt batch jobs when necessary. Batch jobs are scheduled opportunistically and can be paused or rescheduled. This ensures production workload reliability while maintaining high cluster utilization.

**Q4. What’s the difference between designing for portability vs a single environment?**  
A: Designing for portability (like Kubernetes) requires abstraction and flexibility to run on diverse infrastructures. Designing for a single environment (like Borg) allows for deep integration and optimization but limits use to that environment.

---

## Related Trade-offs

### Kubernetes vs Borg
- **Summary:** Kubernetes emphasizes portability and extensibility; Borg emphasizes efficiency and scale for Google.  
- **Trade-off:** Flexibility for diverse environments vs centralized optimization at massive scale.  
- **Questions:** Do you need pluggability and portability? Or extreme utilization within a single environment?  

### Declarative vs Imperative Control
- **Declarative:** Desired state defined; system reconciles differences (Kubernetes, Borg).  
- **Imperative:** Direct commands change system state (legacy orchestration, scripts).  
- **Trade-off:** Simplicity and predictability vs fine-grained control.  

**Q: When would you favor declarative orchestration? How do you handle drift?**  
A: Favor declarative orchestration when you need consistency, repeatability, and automated reconciliation of system state. Declarative models simplify operations and enable self-healing. Drift is handled by continuous reconciliation—controllers detect and correct divergence from the desired state.

### Batch vs Production Workloads
- **Summary:** Batch jobs tolerate preemption and delay; production jobs require strict SLAs.  
- **Trade-off:** Cluster efficiency vs workload isolation.  

**Q: How do you guarantee fairness and avoid starvation across workload types?**  
A: Use priorities and quotas to ensure production workloads are not starved and meet SLAs, while batch jobs can use remaining capacity. Implement preemption and fair scheduling policies to balance efficiency and fairness, preventing batch job starvation.

---

### Interview Checklist Q&A

**Q1. How are workloads scheduled (fairness, bin-packing, priorities)?**  
A: Schedulers use bin-packing to maximize utilization, enforce fairness through quotas and priorities, and support preemption for critical workloads.

**Q2. How do you handle multi-tenancy and quotas?**  
A: Use namespaces for logical isolation, set resource quotas and limits per tenant, and apply RBAC for access control.

**Q3. What happens under node or region failures?**  
A: Orchestrators detect failures and automatically reschedule workloads on healthy nodes or regions, ensuring high availability and minimal disruption.

**Q4. How do orchestration design choices affect utilization and reliability?**  
A: Design choices like centralized vs modular schedulers, bin-packing algorithms, and failure recovery mechanisms directly impact resource efficiency and system reliability.

**Q5. How does declarative orchestration simplify (or complicate) operations?**  
A: Declarative orchestration simplifies operations by automating reconciliation and reducing manual intervention, but can complicate troubleshooting and debugging due to abstraction layers.