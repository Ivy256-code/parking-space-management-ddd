# Domain Model

## Main Domain Concepts

The Parking Space Management System is modelled using Domain-Driven Design (DDD).

### 1. ParkingSpaceNumber

A Value Object representing the unique number assigned to a parking space.

**Responsibility:**
- Validate the parking space number.
- Ensure the number is not empty.
- Maintain a valid parking space number.

---

### 2. ParkingSpace

An Aggregate Root representing a physical parking space.

**Attributes:**
- Parking space number
- Status

**Possible statuses:**
- `AVAILABLE`
- `OCCUPIED`

**Responsibilities:**
- Change its status from `AVAILABLE` to `OCCUPIED`.
- Prevent an occupied space from being assigned again.

---

### 3. ParkingSession

An Aggregate Root representing a customer's active parking session.

**Attributes:**
- Session ID
- Parking space number
- Vehicle category
- Start time
- End time

**Responsibilities:**
- Represent a valid parking session.
- Raise a `ParkingSessionCreated` event after successful creation.

---

### 4. ParkingFeeService

A Domain Service responsible for calculating parking fees.

The fee depends on:

- Parking duration
- Vehicle category
- Applicable parking rate

---

### 5. ParkingSessionCreated

A Domain Event raised when a parking session has been successfully created.

The event contains information needed to identify the affected parking space.

---

### 6. ParkingSpaceRepository

A Repository used to retrieve parking spaces.

**Responsibility:**
- Find a parking space by its number.
- Provide the parking space to the application layer.

---

## Aggregate Boundaries

### ParkingSpace Aggregate

```text
ParkingSpace
     |
     └── ParkingSpaceNumber