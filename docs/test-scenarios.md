# Test Scenarios

## T1 — Valid Parking Space Number

**Given:** A valid parking space number is provided.

**When:** The parking space number is created.

**Then:** The value is accepted.

**Business Rule:** BR1

---

## T2 — Invalid Parking Space Number

**Given:** An empty or incorrectly formatted parking space number is provided.

**When:** The parking space number is created.

**Then:** Validation fails.

**Business Rule:** BR1

---

## T3 — Occupy Available Parking Space

**Given:** A parking space has status `AVAILABLE`.

**When:** A valid parking assignment is accepted.

**Then:** The parking space changes to `OCCUPIED`.

**Business Rule:** BR2

---

## T4 — Reject Assignment to Occupied Space

**Given:** A parking space has status `OCCUPIED`.

**When:** Another active parking session attempts to use it.

**Then:** The assignment is rejected.

**Business Rule:** BR3

---

## T5 — Calculate Parking Fee

**Given:** A parking session has a known duration and vehicle category.

**When:** The parking fee is calculated.

**Then:** The correct fee is returned based on the applicable rate.

**Business Rule:** BR4

---

## T6 — Raise Parking Session Created Event

**Given:** A valid parking session is successfully created.

**When:** The session is created.

**Then:** A `ParkingSessionCreated` event is raised.

**Business Rule:** BR5

---

## T7 — Successful Aggregate Interaction

**Given:**
- A requested parking space exists.
- The parking space is `AVAILABLE`.
- A valid parking session is created.

**When:** The `ParkingSessionCreated` event is handled.

**Then:**
- The parking space is retrieved.
- The parking space changes to `OCCUPIED`.
- The operation completes successfully.

**Business Rules:** BR2, BR5, BR6

---

## T8 — Failed Aggregate Interaction

**Given:**
- A requested parking space exists.
- The parking space is already `OCCUPIED`.

**When:** A new parking session attempts to use the same space.

**Then:**
- The parking space rejects the operation.
- The existing `OCCUPIED` state remains unchanged.
- The new assignment is not completed.

**Business Rule:** BR3

---

## Testing Approach

The project will use `pytest` for automated testing.

Tests will be organized into:

- Domain tests
- Application tests
- Integration tests

The T7 and T8 scenarios will be used to demonstrate interaction between the `ParkingSession` and `ParkingSpace` aggregates.