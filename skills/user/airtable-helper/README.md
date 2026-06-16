# Airtable CRUD Helper

A general-purpose Airtable browser and editor, designed to run as a **Claude artifact** in claude.ai.

## Why this exists

The Airtable MCP `list_records_for_table` tool intermittently fails in claude.ai chat sessions with a compliance error. This artifact bypasses the MCP layer entirely by calling the Airtable REST API directly from the browser.

## Usage

Ask Claude to create an artifact from `airtable_helper.html`, or paste the file contents into a new HTML artifact in claude.ai.

1. Enter your **Airtable Personal Access Token** — it is saved to artifact persistent storage (`window.storage`) and auto-loaded on future uses.
2. Enter a **Base ID** (starts with `app`) and click **load schema** to discover tables and fields.
3. Use the tabs to browse records, create new ones, edit or delete existing ones, or inspect the schema.

## Features

- **Browse**: paginated record list (20 per page), field-based text filter, click any row to edit
- **New record**: schema-aware form with appropriate controls per field type
- **Edit record**: pre-populated form, per-field clear button, save/delete actions
- **Schema**: full table/field inventory with types and options; "use table" button to jump straight to browse

## Token storage

The token is stored in Claude artifact persistent storage — scoped to this artifact, not shared with other artifacts or conversations. It persists across sessions in the same browser profile. You can clear it by entering a blank token and saving.

## Field type support

Handles: singleLineText, multilineText, email, url, number, currency, percent, rating, phoneNumber, singleSelect (dropdown), multipleSelects, checkbox, date, dateTime, richText.

Read-only (displayed but not editable): formula, rollup, count, autoNumber, createdTime, lastModifiedTime, createdBy, lastModifiedBy, multipleLookupValues.

Linked records (multipleRecordLinks) are displayed as record names in browse view.

## Bases in use

| Base | ID | Notes |
|------|----|-------|
| Newsletter Digest | appTDgMZbYXFcYumA | Digest Runs + Newsletter Usage tables |
| Genealogy | (TBD) | Full CRUD |
| Honda Element | appfCLx0oNqwFqiJX | Gas + maintenance logs |
