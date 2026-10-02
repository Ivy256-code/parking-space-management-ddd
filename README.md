# parking-space-management-ddd
A Domain-Driven Design implementation of a Parking Space Management System for coursework.
# Parking Space Management System

## Domain-Driven Design Coursework

A small **Parking Space Management System** developed using **Domain-Driven Design (DDD)** principles.

The purpose of this project is to demonstrate how business rules can be translated into DDD concepts such as **Value Objects, Entities, Aggregate Roots, Aggregates, Domain Services, Domain Events, Repositories, and Application Services**.

---

## 👥 Group Members

| Member       | Responsibility                           |
| ------------ | ---------------------------------------- |
| **Ivy**      | Value Objects & Domain Model             |
| **Ritah**    | ParkingSpace Aggregate                   |
| **Mark**     | ParkingSession & Domain Events           |
| **Julianah** | Services, Repository & Application Layer |

### Shared Responsibilities

All group members will participate in:

* Writing and reviewing tests
* Integration of all components
* T7 and T8 test scenarios
* Documentation
* Code reviews
* GitHub pull requests
* Final testing and debugging

---

# 1. Project Overview

### Problem

The system manages the assignment and occupancy of parking spaces.

A vehicle can request a parking space. The system checks that the requested space exists and can be used. Once a parking session is successfully created, a domain event is raised and handled so that the corresponding parking space becomes occupied.

The system is intentionally kept small so that the focus remains on **Domain-Driven Design and business rules** rather than on building a complete commercial parking application.

---

# 2. Project Objectives

The project aims to:

1. Apply Domain-Driven Design principles.
2. Translate business rules into appropriate DDD concepts.
3. Demonstrate the use of Value Objects.
4. Demonstrate Entities and Aggregate Roots.
5. Protect aggregate invariants.
6. Implement a Domain Service.
7. Implement a Domain Event and Event Handler.
8. Implement a Repository using in-memory persistence.
9. Use an Application Service to coordinate a use case.
10. Write automated tests demonstrating valid and invalid scenarios.

---

# 3. Scope

## In Scope

The system will include:

* Parking spaces
* Parking space numbers
* Vehicles
* Parking sessions
* Parking-space assignment
* Parking-space availability
* Parking-space state changes
* Parking fee calculation
* Domain events
* Event handling
* Repository lookup
* Application services
* Automated tests

## Out of Scope

The following are not required:

* Online payments
* Mobile applications
* GPS/navigation
* Security cameras
* Number-plate recognition
* User authentication
* Notifications
* Production database
* Web interface
* Microservices
* Message brokers
* Cloud deployment

---

# 4. Domain Model

The main domain concepts are:

### Value Object

**ParkingSpaceNumber**

Represents the valid identification number/value of a parking space.

Example:

```text
PS-001
PS-002
PS-003
```

---

### Entities

**ParkingSpace**

Represents a physical parking space and maintains its state.

**ParkingSession**

Represents a parking session created for a vehicle using a parking space.

---

### Aggregate Roots

The system contains two main aggregates:

```text
ParkingSession Aggregate
        │
        │
        ▼
ParkingSpace Aggregate
```

### ParkingSpace Aggregate

```text
ParkingSpace
├── Space ID
├── ParkingSpaceNumber
└── Status
```

Possible states:

```text
AVAILABLE
OCCUPIED
```

### ParkingSession Aggregate

```text
ParkingSession
├── Session ID
├── Vehicle ID
├── Parking Space ID
├── Start Time
└── Session Status
```

---

# 5. Business Rules

The project contains six main business rules. Each rule is mapped to a specific DDD concept.

## BR1 — Value Rule

> A parking space number must follow the required format and must not be empty.

### DDD Concept

**Value Object**

```text
ParkingSpaceNumber
```

### Responsibility

The Value Object validates the parking-space number when it is created.

Example:

```text
PS-001 ✓
PS-025 ✓

""    ✗
ABC   ✗
```

---

## BR2 — Identity / State Rule

> A parking space can change its state from AVAILABLE to OCCUPIED when a valid parking assignment is accepted.

### DDD Concept

**Entity / Aggregate Root**

```text
ParkingSpace
```

The parking space has a unique identity and maintains its own state.

Example:

```text
AVAILABLE
     ↓
OCCUPIED
```

---

## BR3 — Aggregate Invariant

> An OCCUPIED parking space cannot be assigned to another active parking session.

### DDD Concept

**Aggregate Invariant**

The `ParkingSpace` aggregate protects this rule.

The aggregate must reject an attempt to occupy a space that is already occupied.

Example:

```text
ParkingSpace PS-001

Status: OCCUPIED

New request
     ↓
REJECTED
```

---

## BR4 — Cross-Concept Rule

> The parking fee shall be calculated using the parking duration and the applicable vehicle category rate.

### DDD Concept

**Domain Service**

```text
ParkingFeeService
```

The calculation uses information from more than one domain concept.

Conceptually:

```text
Vehicle Category
       +
Parking Duration
       +
Applicable Rate
       ↓
ParkingFeeService
       ↓
Parking Fee
```

---

## BR5 — Follow-Up Rule

> When a parking session is successfully created, a `ParkingSessionCreated` event must be raised so that the corresponding parking space can be requested to change to OCCUPIED.

### DDD Concept

**Domain Event + Event Handler**

The flow is:

```text
ParkingSession
      ↓
ParkingSessionCreated
      ↓
Event Handler
      ↓
ParkingSpace
      ↓
occupy()
```

The `ParkingSession` aggregate does not directly modify the `ParkingSpace` aggregate.

Instead, the domain event communicates that an important business event has occurred.

---

## BR6 — Lookup Rule

> A parking assignment can only proceed if the requested parking space exists and is successfully retrieved from the ParkingSpace repository.

### DDD Concepts

* Repository
* Application Service

The application service requests the parking space from the repository.

```text
Application Service
        ↓
ParkingSpaceRepository
        ↓
Find Parking Space
        ↓
Found?
   ↙         ↘
 YES          NO
  ↓            ↓
Continue     Reject
```

---

# 6. Main Use Case

## Assign Parking Space

The main use case follows this flow:

```text
User Request
     ↓
Application Service
     ↓
Validate / Retrieve Parking Space
     ↓
ParkingSpaceRepository
     ↓
Create ParkingSession
     ↓
ParkingSessionCreated
     ↓
Event Handler
     ↓
ParkingSpace Aggregate
     ↓
Check BR3
     ↓
AVAILABLE → OCCUPIED
```

---

# 7. Aggregate Interaction

The project demonstrates communication between two aggregates.

```text
┌──────────────────────┐
│ ParkingSession       │
│ Aggregate            │
└──────────┬───────────┘
           │
           │ creates
           ▼
┌──────────────────────┐
│ ParkingSessionCreated│
│ Domain Event         │
└──────────┬───────────┘
           │
           │ handled by
           ▼
┌──────────────────────┐
│ Event Handler        │
└──────────┬───────────┘
           │
           │ requests
           ▼
┌──────────────────────┐
│ ParkingSpace         │
│ Aggregate            │
└──────────────────────┘
```

The `ParkingSpace` aggregate is responsible for enforcing its own invariant.

---

# 8. Project Structure

The planned project structure is:

```text
parking-space-management/
│
├── README.md
│
├── docs/
│   ├── business-rules.md
│   ├── domain-model.md
│   └── test-scenarios.md
│
├── src/
│   ├── domain/
│   │   ├── entities/
│   │   ├── value_objects/
│   │   ├── aggregates/
│   │   ├── services/
│   │   └── events/
│   │
│   ├── application/
│   │   ├── services/
│   │   └── dto/
│   │
│   └── infrastructure/
│       └── repositories/
│
├── tests/
│   ├── domain/
│   ├── application/
│   └── integration/
│
└── requirements.txt
```

---

# 9. Division of Work

## 👩 Ivy — Value Objects & Domain Model

### Main responsibility

* Define BR1
* Implement `ParkingSpaceNumber`
* Define the initial domain model
* Help document domain concepts
* Review the overall DDD structure

### Main DDD concepts

```text
Value Object
Entity
Domain Model
```

### Expected work

```text
ParkingSpaceNumber
        ↓
Validation
        ↓
Unit Tests
```

---

## 👩 Ritah — ParkingSpace Aggregate

### Main responsibility

* Define BR2
* Define BR3
* Implement `ParkingSpace`
* Implement the ParkingSpace Aggregate Root
* Implement parking-space state changes
* Protect the aggregate invariant
* Write related unit tests

### Main DDD concepts

```text
Entity
Aggregate
Aggregate Root
Invariant
```

### Expected state transition

```text
AVAILABLE
    ↓
OCCUPIED
```

---

## 👨 Mark — ParkingSession & Domain Events

### Main responsibility

* Define BR5
* Implement `ParkingSession`
* Implement `ParkingSessionCreated`
* Implement event handling
* Connect the ParkingSession aggregate to the ParkingSpace aggregate through the event
* Write related tests

### Main DDD concepts

```text
Aggregate
Domain Event
Event Handler
```

### Expected flow

```text
ParkingSession
      ↓
ParkingSessionCreated
      ↓
Event Handler
      ↓
ParkingSpace
```

---

## 👩 Julianah — Services, Repository & Application Layer

### Main responsibility

* Define BR4
* Define BR6
* Implement `ParkingFeeService`
* Implement `ParkingSpaceRepository`
* Implement in-memory repository
* Implement Application Service
* Implement DTOs where required
* Write related tests

### Main DDD concepts

```text
Domain Service
Repository
Application Service
DTO
```

---

# 10. Shared Testing Responsibilities

Testing is a shared responsibility.

Each member should write tests for the functionality they implement.

The group will also work together on:

### T7 — Successful Scenario

Demonstrate the complete successful flow:

```text
Request
  ↓
Application Service
  ↓
ParkingSession
  ↓
ParkingSessionCreated
  ↓
Event Handler
  ↓
ParkingSpace
  ↓
AVAILABLE → OCCUPIED
  ↓
Successful Result
```

---

### T8 — Failure Scenario

Demonstrate what happens when the follow-up action is rejected.

Example:

```text
ParkingSessionCreated
        ↓
Event Handler
        ↓
ParkingSpace
        ↓
ParkingSpace is already OCCUPIED
        ↓
Reject operation
        ↓
Verify final state + returned outcome
```

The final implementation will clearly document and test the expected outcome of this failure scenario.

---

# 11. Testing Strategy

The project will contain:

### Unit Tests

Used to test individual domain components.

Examples:

```text
ParkingSpaceNumber validation
ParkingSpace state changes
ParkingSpace invariant
ParkingFeeService
ParkingSession
```

### Integration Tests

Used to test interactions between components.

Examples:

```text
Application Service
      ↓
Repository
      ↓
ParkingSession
      ↓
Domain Event
      ↓
Event Handler
      ↓
ParkingSpace
```

---

# 12. GitHub Branching Strategy

The `main` branch will contain the stable version of the project.

Each member will work on a separate feature branch.

```text
main
│
├── feature/ivy-value-object
│
├── feature/ritah-parking-space
│
├── feature/mark-parking-session-events
│
└── feature/julianah-services-repository
```

### Workflow

1. Pull the latest `main`.
2. Create or switch to your feature branch.
3. Implement your assigned work.
4. Write tests.
5. Commit your changes.
6. Push the branch.
7. Create a Pull Request.
8. Another group member reviews the code.
9. Fix any issues identified.
10. Merge into `main`.

---

# 13. Commit Guidelines

Use clear commit messages.

Examples:

```text
feat: add ParkingSpaceNumber value object

feat: implement ParkingSpace aggregate

feat: add ParkingSessionCreated event

feat: implement parking fee service

feat: add parking space repository

test: add ParkingSpace invariant tests

test: add T7 successful scenario

test: add T8 failure scenario

docs: update business rules
```

---

# 14. Definition of Done

A task is considered complete when:

* The required DDD concept has been implemented.
* The relevant business rule is enforced.
* Unit tests have been written.
* Tests pass.
* Code is committed to the member's branch.
* Pull Request is created.
* Another group member reviews the code.
* Changes are merged into `main`.
* Documentation is updated where necessary.

---

# 15. Final Demonstration

The final demonstration should show:

### 1. Domain Model

The main entities, value objects, aggregates and services.

### 2. Business Rules

All six business rules and where they are enforced.

### 3. Successful Flow

```text
Request
 → Application Service
 → Repository
 → ParkingSession
 → Domain Event
 → Event Handler
 → ParkingSpace
 → Success
```

### 4. Failure Flow

```text
Request
 → Application Service
 → ParkingSession
 → Domain Event
 → Event Handler
 → ParkingSpace
 → Invariant Violation
 → Rejection
```

### 5. Automated Tests

Demonstrate the relevant unit and integration tests, including T7 and T8.

---

# 16. Team Goal

The goal of this project is not simply to make a parking system work.

The main goal is to demonstrate how **business rules are translated into a well-structured Domain-Driven Design model**.

The team will therefore prioritize:

```text
Business Rules
       ↓
Domain Concepts
       ↓
DDD Design
       ↓
Implementation
       ↓
Tests
```

---

## Group Members

**Ivy**
Value Objects & Domain Model

**Ritah**
ParkingSpace Aggregate

**Mark**
ParkingSession & Domain Events

**Julianah**
Services, Repository & Application Layer

---

## Status

🚧 **Project in Development**

The repository will be updated progressively as each group member completes and integrates their assigned components.
