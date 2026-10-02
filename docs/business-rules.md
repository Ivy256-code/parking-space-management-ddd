# Business Rules

## BR1 — Parking Space Number Validation

A parking space must have a valid parking space number.

The parking space number:
- Must not be empty.
- Must follow the required parking space number format.

**DDD Concept:** Value Object — `ParkingSpaceNumber`

---

## BR2 — Parking Space Occupancy

A parking space can change from `AVAILABLE` to `OCCUPIED` when a valid parking assignment is accepted.

**DDD Concept:** Entity / Aggregate Root — `ParkingSpace`

---

## BR3 — Occupied Parking Space

An `OCCUPIED` parking space cannot be assigned to another active parking session.

**DDD Concept:** Aggregate Invariant — `ParkingSpace`

---

## BR4 — Parking Fee Calculation

The parking fee is calculated using the parking duration and the applicable vehicle category rate.

**DDD Concept:** Domain Service — `ParkingFeeService`

---

## BR5 — Parking Session Created Event

When a parking session is successfully created, a `ParkingSessionCreated` domain event is raised.

The event allows the corresponding parking space to be requested to change to `OCCUPIED`.

**DDD Concept:** Domain Event — `ParkingSessionCreated`

---

## BR6 — Parking Space Lookup

A parking assignment can only proceed if the requested parking space exists and is successfully retrieved from the parking space repository.

**DDD Concept:** Repository / Application Service