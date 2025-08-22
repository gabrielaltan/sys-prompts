## Database Integration

### System Prompt Snippet

You must add it to the Agent system prompt:

```
Use the tool `Get Base Schema` to load the entire database model (tables, columns, types, policies).  

**Important: Obtain the schema before any other operation by calling `Get Base Schema`!**  
```

### Mandatory Tool

**Get Base Schema**

* **Purpose**: Fetch full schema so the agent understands available tables, fields, and rules.
* **Parameters**

  * `altaner_component_id` (**Hard-coded**): `{{[$vars].room.meta_data.components.base.id}}`
  * `base_id` (**Hard-coded**): Your PostgresSQL project’s base ID (prompt Altan if missing)

### Read Operations

**Query Records**

* **Purpose**: Retrieve rows from a specific table.
* **Parameters**

  * `base_id` (**Hard-coded**)
  * `path` (**Agent**): Target table name
  * `Filter Conditions` (**Agent**): WHERE clause filters
  * `Columns Selection` (**Agent**): List of fields to return

### Write Operations

**Create Records**

* **Purpose**: Insert new rows into a table.
* **Parameters**

  * `base_id` (**Hard-coded**)
  * `path` (**Agent**): Target table name
  * `body` (**Agent**): JSON payload of column-value pairs